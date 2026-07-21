/**
 * @fileoverview AuthButton.jsx - Reusable Authentication Action Button
 * @module components/auth/AuthButton
 * @version 1.0.0
 * @author Antigravity Pair Programmer
 * 
 * Responsibilities:
 * - Render action triggers for form submits.
 * - Manage load/authenticating animation states.
 * - Enforce disable attributes when forms submit.
 * 
 * Exported APIs:
 * - AuthButton (Component)
 */

import React from 'react';

/**
 * Reusable Auth Form Submission Button.
 * 
 * @param {object} props - Component properties.
 * @param {string} props.children - Label text to show.
 * @param {boolean} [props.loading=false] - Whether to show a spinner/loading state.
 * @param {boolean} [props.disabled=false] - Disable trigger flag.
 * @param {string} [props.type='submit'] - Button trigger type.
 * @param {function} [props.onClick] - Trigger click handler callback.
 * @returns {React.JSX.Element} The AuthButton component.
 */
export const AuthButton = ({
  children,
  loading = false,
  disabled = false,
  type = 'submit',
  onClick,
  ...buttonProps
}) => {
  return (
    <button
      type={type}
      disabled={disabled || loading}
      onClick={onClick}
      className={`auth-btn ${loading ? 'auth-btn-loading' : ''}`}
      style={{
        width: '100%',
        padding: '0.85rem 1rem',
        fontSize: '0.95rem',
        fontWeight: 600,
        borderRadius: '0.5rem',
        border: 'none',
        backgroundColor: loading || disabled ? 'rgba(59, 130, 246, 0.5)' : 'var(--color-primary, #3b82f6)',
        color: '#ffffff',
        cursor: loading || disabled ? 'not-allowed' : 'pointer',
        transition: 'background-color 0.2s, transform 0.1s',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '0.5rem',
        outline: 'none',
        boxSizing: 'border-box'
      }}
      {...buttonProps}
    >
      {loading ? (
        <>
          <div 
            className="btn-spinner"
            style={{
              width: '18px',
              height: '18px',
              border: '2px solid rgba(255, 255, 255, 0.3)',
              borderTop: '2px solid #ffffff',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite'
            }}
          />
          <span>Authenticating...</span>
        </>
      ) : (
        children
      )}
    </button>
  );
};
