/**
 * @fileoverview Register.jsx - User Sign-up Page Component (Placeholder)
 * @module pages/Register
 * @version 1.0.0
 * @author Antigravity Pair Programmer
 */

import React from 'react';
import { Link } from 'react-router-dom';
import { AuthLayout } from '../components/auth/AuthLayout.jsx';
import { ROUTE_PATHS } from '../constants/routes.constants.js';

export const Register = () => {
  return (
    <AuthLayout 
      title="Create Account" 
      subtitle="Sign up for SmartRoad AI analytics and driver tracking."
    >
      <div style={{ textAlign: 'center', padding: '1rem', color: 'rgba(255, 255, 255, 0.7)' }}>
        <p>Registration feature is coming soon in the next module phase.</p>
        <p style={{ marginTop: '1.5rem', fontSize: '0.875rem' }}>
          Already have an account?{' '}
          <Link to={ROUTE_PATHS.LOGIN} style={{ color: 'var(--color-primary, #3b82f6)', textDecoration: 'none', fontWeight: 600 }}>
            Sign In
          </Link>
        </p>
      </div>
    </AuthLayout>
  );
};

export default Register;
