import React from 'react';
import { ExpenseStatus } from '../types';

interface StatusBadgeProps {
  status: ExpenseStatus;
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const classes = {
    pending: 'bg-yellow-100 text-yellow-800',
    approved: 'bg-green-100 text-green-800',
    rejected: 'bg-red-100 text-red-800',
    reimbursed: 'bg-blue-100 text-blue-800',
  };

  const labels = {
    pending: 'Pending',
    approved: 'Approved',
    rejected: 'Rejected',
    reimbursed: 'Reimbursed',
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${classes[status]}`}>
      {labels[status]}
    </span>
  );
};