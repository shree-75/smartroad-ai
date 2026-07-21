/**
 * @fileoverview RegisterForm.jsx - Complete Interactive Registration Form Component
 * @module components/auth/RegisterForm
 * @version 1.0.0
 * @author Antigravity Pair Programmer
 * 
 * Responsibilities:
 * - Render registration form fields (name, email, password, confirm password).
 * - Enforce client-side validation rules.
 * - Call the backend registration API via authService.
 * - Provide clean routing redirects and user alerts on completion.
 * 
 * Exported APIs:
 * - RegisterForm (Component)
 */

import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { registerUser } from '../../services/authService.js';
import { 
  validateEmail, 
  validatePassword, 
  validateConfirmPassword, 
  validateFullName 
} from '../../utils/validation.js';
import { FormInput } from './FormInput.jsx';
import { PasswordInput } from './PasswordInput.jsx';
import { AuthButton } from './AuthButton.jsx';
import { ROUTE_PATHS } from '../../constants/routes.constants.js';

/**
 * RegisterForm Component for user signup.
 * 
 * @returns {React.JSX.Element} The RegisterForm component.
 */
export const RegisterForm = () => {
  const navigate = useNavigate();

  // Inputs State
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

  // Status/Flow States
  const [submitting, setSubmitting] = useState(false);
  const [successMessage, setSuccessMessage] = useState('');
  const [apiError, setApiError] = useState('');

  // Field errors State
  const [errors, setErrors] = useState({
    name: null,
    email: null,
    password: null,
    confirmPassword: null
  });

  /**
   * Validates signup fields and submits request payload.
   * 
   * @async
   * @param {React.FormEvent} e - Form event.
   * @returns {Promise<void>}
   */
  const handleSubmit = async (e) => {
    e.preventDefault();
    setApiError('');
    setSuccessMessage('');

    // Trigger validation checks
    const nameVal = validateFullName(name);
    const emailVal = validateEmail(email);
    const passVal = validatePassword(password);
    const confirmVal = validateConfirmPassword(password, confirmPassword);

    setErrors({
      name: nameVal.error,
      email: emailVal.error,
      password: passVal.error,
      confirmPassword: confirmVal.error
    });

    if (!nameVal.isValid || !emailVal.isValid || !passVal.isValid || !confirmVal.isValid) {
      return;
    }

    setSubmitting(true);
    const res = await registerUser({ email, name, password });
    setSubmitting(false);

    if (res.success) {
      setSuccessMessage('Account created successfully! Redirecting to sign in page...');
      setTimeout(() => {
        navigate(ROUTE_PATHS.LOGIN);
      }, 2000);
    } else {
      setApiError(res.error?.message || 'Registration failed. Please try again.');
    }
  };

  return (
    <form onSubmit={handleSubmit} noValidate className="auth-form">
      {/* Success Alert */}
      {successMessage && (
        <div 
          className="auth-alert alert-success"
          role="alert"
          style={{
            padding: '0.75rem 1rem',
            marginBottom: '1.25rem',
            borderRadius: '0.5rem',
            backgroundColor: 'rgba(16, 185, 129, 0.15)',
            border: '1px solid var(--color-success, #10b981)',
            color: 'var(--color-success, #10b981)',
            fontSize: '0.875rem'
          }}
        >
          {successMessage}
        </div>
      )}

      {/* API Server Error Alert */}
      {apiError && (
        <div 
          className="auth-alert alert-danger" 
          role="alert"
          style={{
            padding: '0.75rem 1rem',
            marginBottom: '1.25rem',
            borderRadius: '0.5rem',
            backgroundColor: 'rgba(239, 68, 68, 0.15)',
            border: '1px solid var(--color-error, #ef4444)',
            color: 'var(--color-error, #ef4444)',
            fontSize: '0.875rem'
          }}
        >
          <strong>Registration Error: </strong>
          {apiError}
        </div>
      )}

      {/* Full Name Input */}
      <FormInput
        id="name"
        label="Full Name"
        type="text"
        value={name}
        onChange={(e) => {
          setName(e.target.value);
          if (errors.name) {
            setErrors(prev => ({ ...prev, name: validateFullName(e.target.value).error }));
          }
        }}
        error={errors.name}
        placeholder="Enter your full name"
        required
        disabled={submitting}
        autoComplete="name"
      />

      {/* Email Input */}
      <FormInput
        id="email"
        label="Email Address"
        type="email"
        value={email}
        onChange={(e) => {
          setEmail(e.target.value);
          if (errors.email) {
            setErrors(prev => ({ ...prev, email: validateEmail(e.target.value).error }));
          }
        }}
        error={errors.email}
        placeholder="Enter your email"
        required
        disabled={submitting}
        autoComplete="email"
      />

      {/* Password Input */}
      <PasswordInput
        id="password"
        label="Password"
        value={password}
        onChange={(e) => {
          setPassword(e.target.value);
          if (errors.password) {
            setErrors(prev => ({ ...prev, password: validatePassword(e.target.value).error }));
          }
        }}
        error={errors.password}
        placeholder="Create secure password"
        required
        disabled={submitting}
        autoComplete="new-password"
      />

      {/* Confirm Password Input */}
      <PasswordInput
        id="confirmPassword"
        label="Confirm Password"
        value={confirmPassword}
        onChange={(e) => {
          setConfirmPassword(e.target.value);
          if (errors.confirmPassword) {
            setErrors(prev => ({ ...prev, confirmPassword: validateConfirmPassword(password, e.target.value).error }));
          }
        }}
        error={errors.confirmPassword}
        placeholder="Verify password"
        required
        disabled={submitting}
        autoComplete="new-password"
      />

      {/* Submit Button */}
      <div style={{ marginTop: '1.5rem', marginBottom: '1.5rem' }}>
        <AuthButton loading={submitting} disabled={submitting}>
          Create Account
        </AuthButton>
      </div>

      {/* Direct sign in redirect */}
      <p 
        className="auth-redirect-message"
        style={{
          textAlign: 'center',
          fontSize: '0.875rem',
          margin: 0,
          color: 'rgba(255, 255, 255, 0.6)'
        }}
      >
        Already have an account?{' '}
        <Link 
          to={ROUTE_PATHS.LOGIN} 
          style={{
            color: 'var(--color-primary, #3b82f6)',
            textDecoration: 'none',
            fontWeight: 600
          }}
        >
          Sign In
        </Link>
      </p>
    </form>
  );
};
