/**
 * @fileoverview FormInput.jsx - Standard Reusable Input Form Field
 * @module components/auth/FormInput
 * @version 1.0.0
 * @author Antigravity Pair Programmer
 * 
 * Responsibilities:
 * - Render an input field with label and error messages.
 * - Manage focus, accessibility states (aria properties), and keyboard input.
 * 
 * Exported APIs:
 * - FormInput (Component)
 */

import React from 'react';

/**
 * Standard Form Field Component.
 * 
 * @param {object} props - Component properties.
 * @param {string} props.id - Input field ID (matches html label for).
 * @param {string} props.label - User facing label.
 * @param {string} [props.type='text'] - Input type (email, text, etc.).
 * @param {string} props.value - Controlled input value string.
 * @param {function} props.onChange - Input value handler function.
 * @param {string} [props.error] - Field-level error validation message.
 * @param {string} [props.placeholder] - Help message to show in the field.
 * @param {boolean} [props.required=false] - Field required validation flag.
 * @param {object} [props.inputProps] - Direct input override properties.
 * @returns {React.JSX.Element} The FormInput component.
 */
export const FormInput = ({
  id,
  label,
  type = 'text',
  value,
  onChange,
  error,
  placeholder,
  required = false,
  ...inputProps
}) => {
  const errorId = `${id}-error`;

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
      
      <input
        id={id}
        type={type}
        value={value}
        onChange={onChange}
        placeholder={placeholder}
        required={required}
        aria-invalid={error ? 'true' : 'false'}
        aria-describedby={error ? errorId : undefined}
        className="auth-input"
        style={{
          width: '100%',
          padding: '0.75rem 1rem',
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
