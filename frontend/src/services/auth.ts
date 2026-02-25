import axios, { AxiosResponse } from 'axios';
import { UserCreate, UserLogin, LoginResponse } from '../../../shared/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';
const AUTH_BASE_URL = process.env.NEXT_PUBLIC_BETTER_AUTH_URL || 'http://localhost:8000/auth';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  if (typeof window !== 'undefined') {
  const token = localStorage.getItem('access_token');
   if (token) {
    config.headers.Authorization = `Bearer ${token}`;
   }
  }
  return config;
});

const authHeaders = { 'Content-Type': 'application/json' };

// Register a new user
export const registerUser = async (userData: UserCreate): Promise<AxiosResponse<any>> => {
  try {
    const response = await axios.post(`${AUTH_BASE_URL}/register`, userData, {
      headers: authHeaders,
    });
    return response;
  } catch (error) {
    throw error;
  }
};

// Login user
export const loginUser = async (credentials: UserLogin): Promise<LoginResponse> => {
  try {
    const response = await axios.post(`${AUTH_BASE_URL}/login`, {
      email: credentials.email,
      password: credentials.password
    }, { headers: authHeaders });

    // Store the token in localStorage
    if (response.data.access_token) {
      localStorage.setItem('access_token', response.data.access_token);
    }

    return response.data;
  } catch (error) {
    throw error;
  }
};

// Logout user
export const logoutUser = (): void => {
  if (typeof window === 'undefined') return;
  localStorage.removeItem('access_token');
};

// Check if user is authenticated
export const isAuthenticated = (): boolean => {
  if (typeof window === 'undefined') return false;
  return!! localStorage.getItem('access_token');
};

// Get current user ID from token (basic decoding, not for security purposes)
export const getCurrentUserId = (): number | null => {
  if (typeof window === 'undefined') return null;
  const token = localStorage.getItem('access_token');
  if (!token) return null;

  try {
    const payload = token.split('.')[1];
    const decodedPayload = JSON.parse(atob(payload));
    return decodedPayload.sub ? parseInt(decodedPayload.sub) : null;
  } catch (error) {
    console.error('Error decoding token:', error);
    return null;
  }
};