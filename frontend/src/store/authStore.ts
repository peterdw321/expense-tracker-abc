import { create } from 'zustand';
import { User } from '../types';
import { authApi } from '../services/api';

interface AuthState {
  user: User | null;
  token: string | null;
  isLoading: boolean;
  error: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: localStorage.getItem('access_token'),
  isLoading: false,
  error: null,

  login: async (email: string, password: string) => {
    set({ isLoading: true, error: null });
    try {
      const { data } = await authApi.login(email, password);
      localStorage.setItem('access_token', data.access_token);
      const { data: userData } = await authApi.me();
      set({ user: userData, token: data.access_token, isLoading: false });
    } catch (error: unknown) {
      const err = error as { response?: { data?: { detail?: string | Record<string, unknown> } } };
      let errorMessage = 'Login failed';
      const detail = err.response?.data?.detail;
      if (typeof detail === 'string') {
        errorMessage = detail;
      } else if (detail && typeof detail === 'object' && 'msg' in detail) {
        errorMessage = String(detail.msg);
      }
      set({ 
        isLoading: false, 
        error: errorMessage 
      });
      throw error;
    }
  },

  logout: () => {
    localStorage.removeItem('access_token');
    set({ user: null, token: null });
  },

  checkAuth: async () => {
    const token = localStorage.getItem('access_token');
    if (!token) {
      set({ user: null, token: null });
      return;
    }
    try {
      const { data } = await authApi.me();
      set({ user: data, token });
    } catch {
      localStorage.removeItem('access_token');
      set({ user: null, token: null });
    }
  },
}));