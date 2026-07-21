/**
 * @fileoverview App.jsx - Main Application Component and Router Config
 * @module App
 * @version 1.0.0
 * @author Antigravity Pair Programmer
 * 
 * Responsibilities:
 * - Wrap application inside AuthProvider container.
 * - Establish react-router router endpoints.
 * - Guard routes using ProtectedRoute and PublicRoute component filters.
 * 
 * Exported APIs:
 * - App (Component)
 */

import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext.jsx';
import { ProtectedRoute } from './components/auth/ProtectedRoute.jsx';
import { PublicRoute } from './components/auth/PublicRoute.jsx';
import { Login } from './pages/Login.jsx';
import { Register } from './pages/Register.jsx';
import { Dashboard } from './pages/Dashboard.jsx';
import { ROUTE_PATHS } from './constants/routes.constants.js';

export const App = () => {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          {/* Public Authentication Views */}
          <Route element={<PublicRoute />}>
            <Route path={ROUTE_PATHS.LOGIN} element={<Login />} />
            <Route path={ROUTE_PATHS.REGISTER} element={<Register />} />
          </Route>

          {/* Protected Main Views */}
          <Route element={<ProtectedRoute />}>
            <Route path={ROUTE_PATHS.DASHBOARD} element={<Dashboard />} />
          </Route>

          {/* Root Redirection */}
          <Route path="/" element={<Navigate to={ROUTE_PATHS.DASHBOARD} replace />} />
          <Route path="*" element={<Navigate to={ROUTE_PATHS.LOGIN} replace />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  );
};

export default App;