'use client';
import React from 'react';
import Link from 'next/link';

export default function Home() {
  return (
    <div style={{ padding: '2rem', textAlign: 'center' }}>
      <h1>Welcome to the Todo App</h1>
      <p>Your secure, multi-user todo management application</p>
      <div style={{ marginTop: '2rem' }}>
        <Link href="/login" style={{ marginRight: '1rem', textDecoration: 'none', color: '#0070f3' }}>
          <button>Login</button>
        </Link>
        <Link href="/register" style={{ textDecoration: 'none', color: '#0070f3' }}>
          <button>Register</button>
        </Link>
      </div>
    </div>
  );
}