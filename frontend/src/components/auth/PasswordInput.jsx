/**
 * @fileoverview PasswordInput.jsx - Reusable Password Input Field with Show/Hide Toggle
 * @module components/auth/PasswordInput
 * @version 1.0.0
 * @author Antigravity Pair Programmer
 * 
 * Responsibilities:
 * - Render secure password input fields.
 * - Toggle password visibility between dots and plaintext.
 * - Support accessibility attributes and error layouts.
 * 
 * Exported APIs:
 * - PasswordInput (Component)
 */

import React, { useState } from 'react';

/**
 * Reusable Password Field with visibility controls.
 * 
 * @param {object} props - Component properties.
 * @param {string} props.id - Input field ID.
 * @param {string} props.label - User facing label.
 * @param {string} props.value - Controlled input value.
 * @param {function} props.onChange - Input value handler function.
 * @param {string} [props.error] - Field-level validation error message.
 * @param {string} [props.placeholder='••••••••'] - Help placeholder string.
 * @param {boolean} [props.required=false] - Field required validation flag.
 * @returns {React.JSX.Element} The PasswordInput component.
 */
export const PasswordInput = ({
  id,
  label,
  value,
  onChange,
  error,
  placeholder = '••••••••',
  required = false,
  ...inputProps
}) => {
  const [showPassword, setShowPassword] = useState(false);
  const errorId = `${id}-error`;

  const toggleVisibility = () => {
    setShowPassword((prev) => !prev);
  };

  return (
    <div className={`auth-form-group ${error ? 'has-error' : ''}`} style={{ marginBottom: '1.25rem' }}>
      <label 
        htmlFor={id} 
        className="auth-label"
        style={{
          display: 'block',
          marginBottom: '0.5rem',
          fontSize: '0.85rem',
          fontWeight: 500,
          color: 'var(--color-text, #f3f4f6)'
        }}
      >
        {label} {required && <span className="required-indicator" style={{ color: 'var(--color-error, #ef4444)' }}>*</span>}
      </label>
      
      <div className="password-input-wrapper" style={{ position: 'relative' }}>
        <input
          id={id}
          type={showPassword ? 'text' : 'password'}
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          required={required}
          aria-invalid={error ? 'true' : 'false'}
          aria-describedby={error ? errorId : undefined}
          className="auth-input password-input-field"
          style={{
            width: '100%',
            padding: '0.75rem 2.75rem 0.75rem 1rem',
            fontSize: '0.95rem',
            borderRadius: '0.5rem',
            border: error ? '1px solid var(--color-error, #ef4444)' : '1px solid rgba(255, 255, 255, 0.1)',
            backgroundColor: 'rgba(255, 255, 255, 0.05)',
            color: 'var(--color-text, #f3f4f6)',
            outline: 'none',
            boxSizing: 'border-box',
            transition: 'border-color 0.2s, box-shadow 0.2s'
          }}
          {...inputProps}
        />
        
        <button
          type="button"
          onClick={toggleVisibility}
          aria-label={showPassword ? 'Hide password' : 'Show password'}
          className="password-toggle-btn"
          style={{
            position: 'absolute',
            right: '0.75rem',
            top: '50%',
            transform: 'translateY(-50%)',
            background: 'none',
            border: 'none',
            color: 'rgba(255, 255, 255, 0.5)',
            cursor: 'pointer',
            padding: '0.25rem',
            fontSize: '0.85rem',
            outline: 'none',
            userSelect: 'none'
          }}
        >
          {showPassword ? 'Hide' : 'Show'}
        </button>
      </div>

      {error && (
        <span 
          id={errorId} 
          className="auth-error-message"
          role="alert"
          style={{
            display: 'block',
            marginTop: '0.35rem',
            fontSize: '0.8rem',
            color: 'var(--color-error, #ef4444)'
          }}
        >
          {error}
        </span>
      )}
    </div>
  );
};
