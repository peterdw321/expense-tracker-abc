import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';
import { expensesApi } from '../services/api';
import { Expense } from '../types';
import { StatusBadge } from '../components/StatusBadge';
import { Button } from '../components/Button';

export const ExpenseDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user } = useAuthStore();
  const [expense, setExpense] = useState<Expense | null>(null);
  const [loading, setLoading] = useState(true);
  const [actionLoading, setActionLoading] = useState(false);
  const [rejectReason, setRejectReason] = useState('');

  useEffect(() => {
    const fetchExpense = async () => {
      try {
        const { data } = await expensesApi.get(id!);
        setExpense(data);
      } catch (error) {
        console.error('Failed to fetch expense:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchExpense();
  }, [id]);

  const handleApprove = async () => {
    setActionLoading(true);
    try {
      await expensesApi.approve(id!);
      navigate(0);
    } catch (error) {
      console.error('Failed to approve expense:', error);
    } finally {
      setActionLoading(false);
    }
  };

  const handleReject = async () => {
    if (!rejectReason.trim()) return;
    setActionLoading(true);
    try {
      await expensesApi.reject(id!, rejectReason);
      navigate(0);
    } catch (error) {
      console.error('Failed to reject expense:', error);
    } finally {
      setActionLoading(false);
    }
  };

  const handleReimburse = async () => {
    setActionLoading(true);
    try {
      await expensesApi.reimburse(id!);
      navigate(0);
    } catch (error) {
      console.error('Failed to reimburse expense:', error);
    } finally {
      setActionLoading(false);
    }
  };

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);

  const formatDate = (date: string) =>
    new Date(date).toLocaleDateString('en-US', {
      month: 'long',
      day: 'numeric',
      year: 'numeric',
      hour: 'numeric',
      minute: '2-digit',
    });

  if (loading) return <div className="text-center py-8">Loading...</div>;
  if (!expense) return <div className="text-center py-8">Expense not found</div>;

  const canApprove = user?.role === 'manager' || user?.role === 'finance';
  const canReject = user?.role === 'manager' || user?.role === 'finance';
  const canReimburse = user?.role === 'finance';

  return (
    <div className="max-w-3xl">
      <Button variant="outline" onClick={() => navigate('/expenses')} className="mb-4">
        Back to Expenses
      </Button>

      <div className="card">
        <div className="p-6 border-b border-gray-100">
          <div className="flex justify-between items-start mb-4">
            <h1 className="text-2xl font-bold font-heading">{expense.title}</h1>
            <StatusBadge status={expense.status} />
          </div>
          <p className="text-text-secondary">Submitted on {formatDate(expense.submitted_at)}</p>
        </div>

        <div className="p-6 space-y-6">
          <div className="grid grid-cols-2 gap-6">
            <div>
              <p className="text-sm text-text-secondary mb-1">Category</p>
              <p className="font-medium capitalize">{expense.category}</p>
            </div>
            <div>
              <p className="text-sm text-text-secondary mb-1">Amount</p>
              <p className="font-medium text-xl">{formatCurrency(expense.amount)}</p>
            </div>
          </div>

          {expense.description && (
            <div>
              <p className="text-sm text-text-secondary mb-1">Description</p>
              <p>{expense.description}</p>
            </div>
          )}

          {expense.rejection_reason && (
            <div className="p-4 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm font-medium text-error mb-1">Rejection Reason</p>
              <p className="text-text-primary">{expense.rejection_reason}</p>
            </div>
          )}

          {expense.reviewed_at && (
            <div className="text-sm text-text-secondary">
              Reviewed on {formatDate(expense.reviewed_at)}
            </div>
          )}
        </div>

        {(canApprove || canReject || canReimburse) && expense.status === 'pending' && (
          <div className="p-6 border-t border-gray-100">
            <div className="flex gap-4">
              {canApprove && (
                <Button onClick={handleApprove} isLoading={actionLoading}>
                  Approve
                </Button>
              )}
              {canReject && (
                <div className="flex-1">
                  <textarea
                    className="w-full px-3 py-2 border border-gray-300 rounded-md mb-2"
                    rows={2}
                    placeholder="Rejection reason (required)"
                    value={rejectReason}
                    onChange={(e) => setRejectReason(e.target.value)}
                  />
                  <Button variant="danger" onClick={handleReject} disabled={!rejectReason.trim()}>
                    Reject
                  </Button>
                </div>
              )}
            </div>
          </div>
        )}

        {canReimburse && expense.status === 'approved' && (
          <div className="p-6 border-t border-gray-100">
            <Button onClick={handleReimburse} isLoading={actionLoading}>
              Mark as Reimbursed
            </Button>
          </div>
        )}
      </div>
    </div>
  );
};