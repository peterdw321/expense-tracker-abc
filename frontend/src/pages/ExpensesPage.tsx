import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { expensesApi } from '../services/api';
import { Expense } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { Button } from '../components/Button';
import { Select } from '../components/Select';

export const ExpensesPage: React.FC = () => {
  const navigate = useNavigate();
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [loading, setLoading] = useState(true);
  const [statusFilter, setStatusFilter] = useState<string>('');

  useEffect(() => {
    const fetchExpenses = async () => {
      try {
        const params = statusFilter ? { status: statusFilter } : {};
        const { data } = await expensesApi.list(params);
        setExpenses(data);
      } catch (error) {
        console.error('Failed to fetch expenses:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchExpenses();
  }, [statusFilter]);

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);

  const formatDate = (date: string) =>
    new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

  const statusOptions = [
    { value: '', label: 'All Statuses' },
    { value: 'pending', label: 'Pending' },
    { value: 'approved', label: 'Approved' },
    { value: 'rejected', label: 'Rejected' },
    { value: 'reimbursed', label: 'Reimbursed' },
  ];

  if (loading) return <div className="text-center py-8">Loading...</div>;

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold font-heading">Expenses</h1>
        <Button onClick={() => navigate('/expenses/new')}>Submit New Expense</Button>
      </div>

      <div className="card mb-6">
        <div className="p-4">
          <div className="flex gap-4">
            <div className="w-48">
              <Select
                options={statusOptions}
                value={statusFilter}
                onChange={(e) => setStatusFilter(e.target.value)}
              />
            </div>
          </div>
        </div>
      </div>

      <div className="card overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-4 py-3 text-left text-xs font-medium text-text-secondary uppercase">Date</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-text-secondary uppercase">Title</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-text-secondary uppercase">Category</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-text-secondary uppercase">Amount</th>
                <th className="px-4 py-3 text-left text-xs font-medium text-text-secondary uppercase">Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-100">
              {expenses.length === 0 ? (
                <tr>
                  <td colSpan={5} className="px-4 py-8 text-center text-text-secondary">
                    No expenses found
                  </td>
                </tr>
              ) : (
                expenses.map((expense) => (
                  <tr
                    key={expense.id}
                    className="hover:bg-gray-50 cursor-pointer"
                    onClick={() => navigate(`/expenses/${expense.id}`)}
                  >
                    <td className="px-4 py-3">{formatDate(expense.submitted_at)}</td>
                    <td className="px-4 py-3">{expense.title}</td>
                    <td className="px-4 py-3 capitalize">{expense.category}</td>
                    <td className="px-4 py-3 font-medium">{formatCurrency(expense.amount)}</td>
                    <td className="px-4 py-3">
                      <StatusBadge status={expense.status} />
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};