'use client';
import React from 'react';
import { useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { isAuthenticated } from '../services/auth';

interface ProtectedRouteProps {
  children: React.ReactNode;
}

export default function ProtectedRoute({ children }: ProtectedRouteProps) {
  const router = useRouter();

  useEffect(() => {
    if (!isAuthenticated()) {
      // Redirect to login if not authenticated
      router.push('/login');
    }
  }, [router]);

  // If not authenticated, don't render anything (redirect will happen)
  if (!isAuthenticated()) {
    return <div>Redirecting...</div>;
  }

  // If authenticated, render the protected content
  return <>{children}</>;
}