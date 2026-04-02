import axios from 'axios';

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'https://expense-tracker-production-0757.up.railway.app/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authApi = {
  login: (email: string, password: string) =>
    api.post('/auth/login', 
      `username=${encodeURIComponent(email)}&password=${encodeURIComponent(password)}`,
      {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      }
    ),
  register: (data: { email: string; password: string; full_name: string; role: string; department?: string }) =>
    api.post('/auth/register', data),
  me: () => api.get('/auth/me'),
};

export const usersApi = {
  list: () => api.get('/users'),
  get: (id: string) => api.get(`/users/${id}`),
  update: (id: string, data: { full_name?: string; department?: string }) =>
    api.put(`/users/${id}`, data),
};

export const expensesApi = {
  list: (params?: { skip?: number; limit?: number; status?: string }) =>
    api.get('/expenses', { params }),
  create: (data: { title: string; description?: string; amount: number; category: string; receipt_url?: string }) =>
    api.post('/expenses', data),
  get: (id: string) => api.get(`/expenses/${id}`),
  update: (id: string, data: { title?: string; description?: string; amount?: number; category?: string }) =>
    api.put(`/expenses/${id}`, data),
  delete: (id: string) => api.delete(`/expenses/${id}`),
  approve: (id: string) => api.post(`/expenses/${id}/approve`),
  reject: (id: string, reason: string) => api.post(`/expenses/${id}/reject`, { reason }),
  reimburse: (id: string) => api.post(`/expenses/${id}/reimburse`),
};

export const reportsApi = {
  summary: () => api.get('/reports/summary'),
  byCategory: () => api.get('/reports/by-category'),
  byDepartment: () => api.get('/reports/by-department'),
};

export default api;