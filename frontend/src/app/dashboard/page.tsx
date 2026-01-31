'use client';
import React, { useState } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated, logoutUser } from '../../services/auth';
import ProtectedRoute from '../../components/ProtectedRoute';
import TodoList from '../../components/TodoList';
import TodoForm from '../../components/TodoForm';

export default function DashboardPage() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const router = useRouter();

  const handleLogout = () => {
    logoutUser();
    router.push('/login');
  };

  const handleTodoUpdate = () => {
    // Trigger a refresh by updating the state
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <ProtectedRoute>
      <div style={{ padding: '2rem', maxWidth: '800px', margin: '0 auto' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '2rem' }}>
          <h1>Todo Dashboard</h1>
          <button
            onClick={handleLogout}
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#ff4444',
              color: 'white',
              border: 'none',
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Logout
          </button>
        </div>

        <TodoForm onTodoCreated={handleTodoUpdate} />

        <div style={{ marginTop: '2rem' }}>
          <TodoList key={refreshTrigger} onTodoUpdate={handleTodoUpdate} />
        </div>
      </div>
    </ProtectedRoute>
  );
}