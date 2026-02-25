import axios, { AxiosResponse } from 'axios';
import { Todo, TodoCreate, TodoUpdate } from '../../../shared/types/api';

const API_BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Get all todos for a user
export const getUserTodos = async (userId: number): Promise<Todo[]> => {
  try {
    const response = await api.get<Todo[]>(`/${userId}/tasks`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Get a specific todo
export const getTodoById = async (userId: number, todoId: number): Promise<Todo> => {
  try {
    const response = await api.get<Todo>(`/${userId}/tasks/${todoId}`);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Create a new todo
export const createTodo = async (userId: number, todoData: TodoCreate): Promise<Todo> => {
  try {
    const response = await api.post<Todo>(`/${userId}/tasks`, todoData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Update a todo
export const updateTodo = async (userId: number, todoId: number, todoData: TodoUpdate): Promise<Todo> => {
  try {
    const response = await api.put<Todo>(`/${userId}/tasks/${todoId}`, todoData);
    return response.data;
  } catch (error) {
    throw error;
  }
};

// Delete a todo
export const deleteTodo = async (userId: number, todoId: number): Promise<void> => {
  try {
    await api.delete(`/${userId}/tasks/${todoId}`);
  } catch (error) {
    throw error;
  }
};

// Toggle todo completion status
export const toggleTodoCompletion = async (userId: number, todoId: number): Promise<Todo> => {
  try {
    const response = await api.patch<Todo>(`/${userId}/tasks/${todoId}/complete`, {
      completed: true // The backend handles toggling internally
    });
    return response.data;
  } catch (error) {
    throw error;
  }
};