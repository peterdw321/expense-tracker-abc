import React from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useAuthStore } from '../store/authStore';

interface LayoutProps {
  children: React.ReactNode;
}

export const Layout: React.FC<LayoutProps> = ({ children }) => {
  const { user, logout } = useAuthStore();
  const location = useLocation();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const navItems = [
    { path: '/dashboard', label: 'Dashboard', roles: ['employee', 'manager', 'finance'] },
    { path: '/expenses', label: 'Expenses', roles: ['employee', 'manager', 'finance'] },
    { path: '/reports', label: 'Reports', roles: ['manager', 'finance'] },
  ];

  const filteredNavItems = navItems.filter(
    (item) => user && item.roles.includes(user.role)
  );

  return (
    <div className="min-h-screen bg-background">
      <header className="bg-primary text-white shadow-md">
        <div className="max-w-7xl mx-auto px-4 py-4 flex items-center justify-between">
          <Link to="/dashboard" className="text-xl font-bold font-heading">
            ABC Corp Expenses
          </Link>
          <nav className="flex items-center gap-6">
            {filteredNavItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`hover:text-accent transition-colors ${
                  location.pathname === item.path ? 'text-accent' : ''
                }`}
              >
                {item.label}
              </Link>
            ))}
            <div className="flex items-center gap-4">
              <span className="text-sm text-gray-200">{user?.full_name}</span>
              <button
                onClick={handleLogout}
                className="text-sm hover:text-accent transition-colors"
              >
                Logout
              </button>
            </div>
          </nav>
        </div>
      </header>
      <main className="max-w-7xl mx-auto px-4 py-8">{children}</main>
    </div>
  );
};