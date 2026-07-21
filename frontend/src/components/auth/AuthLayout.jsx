/**
 * @fileoverview AuthLayout.jsx - Reusable Layout Wrapper for Authentication Pages
 * @module components/auth/AuthLayout
 * @version 1.0.0
 * @author Antigravity Pair Programmer
 * 
 * Responsibilities:
 * - Wrap authentication form panels (login, register, reset-password).
 * - Render branding elements (SmartRoad AI logotype, description).
 * - Implement premium glassmorphic visual styles via Auth.css.
 * 
 * Exported APIs:
 * - AuthLayout (Component)
 */

import React from 'react';
import '../../styles/Auth.css';

/**
 * Common layout panel wrapping authentication views with consistent branding and styling.
 * 
 * @param {object} props - Component properties.
 * @param {React.ReactNode} props.children - Child nodes representing the login form, etc.
 * @param {string} [props.title] - Title heading.
 * @param {string} [props.subtitle] - Subtitle description.
 * @returns {React.JSX.Element} The AuthLayout component.
 */
export const AuthLayout = ({ children, title, subtitle }) => {
  return (
    <div className="auth-page">
      <div className="auth-container">
        {/* Brand Header */}
        <div className="auth-header">
          <div className="auth-brand">
            <span className="auth-logo-icon">🚗</span>
            <h1 className="auth-logo-text">SmartRoad <span className="logo-accent">AI</span></h1>
          </div>
          {title && <h2 className="auth-title">{title}</h2>}
          {subtitle && <p className="auth-subtitle">{subtitle}</p>}
        </div>

        {/* Content Box */}
        <div className="auth-card">
          {children}
        </div>

        {/* Footer Brand Info */}
        <div className="auth-footer-branding">
          <p>© {new Date().getFullYear()} SmartRoad AI. Precision Analytics & Road Safety.</p>
        </div>
      </div>
    </div>
  );
};
