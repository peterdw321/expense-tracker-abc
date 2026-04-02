import React, { useEffect, useState } from 'react';
import { reportsApi } from '../services/api';
import { ReportSummary, ReportByCategory, ReportByDepartment } from '../types';

export const ReportsPage: React.FC = () => {
  const [summary, setSummary] = useState<ReportSummary | null>(null);
  const [byCategory, setByCategory] = useState<ReportByCategory[]>([]);
  const [byDepartment, setByDepartment] = useState<ReportByDepartment[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const [summaryRes, categoryRes, departmentRes] = await Promise.all([
          reportsApi.summary(),
          reportsApi.byCategory(),
          reportsApi.byDepartment(),
        ]);
        setSummary(summaryRes.data);
        setByCategory(categoryRes.data);
        setByDepartment(departmentRes.data);
      } catch (error) {
        console.error('Failed to fetch reports:', error);
      } finally {
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  const formatCurrency = (amount: number) =>
    new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);

  if (loading) return <div className="text-center py-8">Loading...</div>;

  return (
    <div>
      <h1 className="text-2xl font-bold font-heading mb-6">Reports</h1>

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

      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="card">
          <div className="p-4 border-b border-gray-100">
            <h2 className="text-lg font-semibold font-heading">By Category</h2>
          </div>
          <div className="p-4">
            {byCategory.length === 0 ? (
              <p className="text-text-secondary">No data available</p>
            ) : (
              <div className="space-y-3">
                {byCategory.map((item) => (
                  <div key={item.category} className="flex justify-between items-center">
                    <span className="capitalize">{item.category}</span>
                    <div className="text-right">
                      <p className="font-medium">{formatCurrency(item.total)}</p>
                      <p className="text-sm text-text-secondary">{item.count} expenses</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>

        <div className="card">
          <div className="p-4 border-b border-gray-100">
            <h2 className="text-lg font-semibold font-heading">By Department</h2>
          </div>
          <div className="p-4">
            {byDepartment.length === 0 ? (
              <p className="text-text-secondary">No data available</p>
            ) : (
              <div className="space-y-3">
                {byDepartment.map((item) => (
                  <div key={item.department} className="flex justify-between items-center">
                    <span>{item.department}</span>
                    <div className="text-right">
                      <p className="font-medium">{formatCurrency(item.total)}</p>
                      <p className="text-sm text-text-secondary">{item.count} expenses</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};