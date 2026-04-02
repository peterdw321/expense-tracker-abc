import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { expensesApi, reportsApi } from '../services/api';
import { Expense, ReportSummary } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { Button } from '../components/Button';

export const DashboardPage: React.FC = () => {
  const { user } = useAuthStore();
  const navigate = useNavigate();
  const [expenses, setExpenses] = useState<Expense[]>([]);
  const [summary, setSummary] = useState<ReportSummary | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [expensesRes, summaryRes] = await Promise.all([
          expensesApi.list({ limit: 5 }),
          user?.role !== 'employee' ? reportsApi.summary() : Promise.resolve(null),
        ]);
        setExpenses(expensesRes.data);
        if (summaryRes) setSummary(summaryRes.data);
      } catch (error) {
        console.error('Failed to fetch data:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, [user?.role]);

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);

  const formatDate = (date: string) =>
    new Date(date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });

  if (loading) return <div className="text-center py-8">Loading...</div>;

  return (
    <div>
      <div className="mb-8">
        <h1 className="text-2xl font-bold font-heading">Welcome, {user?.full_name}</h1>
        <p className="text-text-secondary capitalize">{user?.role} Dashboard</p>
      </div>

      {user?.role === 'employee' && (
        <div className="mb-8">
          <Button onClick={() => navigate('/expenses/new')}>Submit New Expense</Button>
        </div>
      )}

      {summary && (
        <div className="grid grid-cols-1 md:grid-cols-5 gap-4 mb-8">
          <div className="card p-4">
            <p className="text-sm text-text-secondary">Total Expenses</p>
            <p className="text-2xl font-bold">{formatCurrency(summary.total_expenses)}</p>
          </div>
          <div className="card p-4">
            <p className="text-sm text-text-secondary">Pending</p>
            <p className="text-2xl font-bold text-warning">{summary.pending_count}</p>
          </div>
          <div className="card p-4">
            <p className="text-sm text-text-secondary">Approved</p>
            <p className="text-2xl font-bold text-success">{summary.approved_count}</p>
          </div>
          <div className="card p-4">
            <p className="text-sm text-text-secondary">Rejected</p>
            <p className="text-2xl font-bold text-error">{summary.rejected_count}</p>
          </div>
          <div className="card p-4">
            <p className="text-sm text-text-secondary">Reimbursed</p>
            <p className="text-2xl font-bold text-secondary">{summary.reimbursed_count}</p>
          </div>
        </div>
      )}

      <div className="card">
        <div className="p-4 border-b border-gray-100 flex justify-between items-center">
          <h2 className="text-lg font-semibold font-heading">Recent Expenses</h2>
          <Button variant="outline" onClick={() => navigate('/expenses')}>
            View All
          </Button>
        </div>
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
                    No expenses yet
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