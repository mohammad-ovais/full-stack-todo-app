'use client';
import React, { useState, useEffect } from 'react';
import { Todo } from '../../../shared/types/api';
import { getUserTodos, deleteTodo, toggleTodoCompletion } from '../services/api';
import { getCurrentUserId } from '../services/auth';

interface TodoListProps {
  onTodoUpdate: () => void;
}

export default function TodoList({ onTodoUpdate }: TodoListProps) {
  const [todos, setTodos] = useState<Todo[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [updatingTodoIds, setUpdatingTodoIds] = useState<number[]>([]); // Track which todos are being updated

  const userId = getCurrentUserId();

  useEffect(() => {
    if (userId) {
      fetchTodos();
    }
  }, [userId, onTodoUpdate]); // Fetch todos when userId changes or when onTodoUpdate is called

  const fetchTodos = async () => {
    if (!userId) return;

    try {
      setLoading(true);
      const userTodos = await getUserTodos(userId);
      setTodos(userTodos);
      setError('');
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to fetch todos');
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (todoId: number) => {
    if (!userId) return;

    try {
      await deleteTodo(userId, todoId);
      // Refresh the todo list after deletion
      fetchTodos();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to delete todo');
    }
  };

  const handleToggleCompletion = async (todo: Todo) => {
    if (!userId) return;

    // Add to updating list
    setUpdatingTodoIds(prev => [...prev, todo.id]);

    try {
      await toggleTodoCompletion(userId, todo.id);
      // Refresh the todo list after toggling
      fetchTodos();
    } catch (err: any) {
      setError(err.response?.data?.detail || 'Failed to update todo');
    } finally {
      // Remove from updating list
      setUpdatingTodoIds(prev => prev.filter(id => id !== todo.id));
    }
  };

  if (loading) return <div>Loading todos...</div>;
  if (error) {
    return (
      <div>
        <div style={{ color: 'red', marginBottom: '1rem' }}>Error: {error}</div>
        <button
          onClick={fetchTodos}
          style={{
            padding: '0.5rem 1rem',
            backgroundColor: '#0070f3',
            color: 'white',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Retry
        </button>
      </div>
    );
  }

  return (
    <div>
      <h3>Your Todos</h3>
      {todos.length === 0 ? (
        <p>No todos yet. Add one to get started!</p>
      ) : (
        <ul style={{ listStyle: 'none', padding: 0 }}>
          {todos.map(todo => (
            <li
              key={todo.id}
              style={{
                borderBottom: '1px solid #eee',
                padding: '1rem 0',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center'
              }}
            >
              <div>
                <input
                  type="checkbox"
                  checked={todo.completed}
                  onChange={() => handleToggleCompletion(todo)}
                  disabled={updatingTodoIds.includes(todo.id)} // Disable during update
                  style={{ marginRight: '0.5rem' }}
                />
                <span
                  style={{
                    textDecoration: todo.completed ? 'line-through' : 'none',
                    color: todo.completed ? '#888' : 'inherit'
                  }}
                >
                  {todo.title}
                </span>
                {todo.description && (
                  <div style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.25rem' }}>
                    {todo.description}
                  </div>
                )}
              </div>
              <div>
                <button
                  onClick={() => handleDelete(todo.id)}
                  disabled={updatingTodoIds.includes(todo.id)} // Disable during other updates
                  style={{
                    backgroundColor: updatingTodoIds.includes(todo.id) ? '#cccccc' : '#ff4444',
                    color: 'white',
                    border: 'none',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    cursor: updatingTodoIds.includes(todo.id) ? 'not-allowed' : 'pointer'
                  }}
                >
                  {updatingTodoIds.includes(todo.id) ? 'Deleting...' : 'Delete'}
                </button>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}