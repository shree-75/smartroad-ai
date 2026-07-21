/**
 * @fileoverview Dashboard.jsx - Protected Dashboard Page Component
 * @module pages/Dashboard
 * @version 1.0.0
 * @author Antigravity Pair Programmer
 * 
 * Responsibilities:
 * - Render private dashboard telemetry indicators.
 * - Expose sign-out button triggers.
 * 
 * Exported APIs:
 * - Dashboard (Component)
 */

import React from 'react';
import { useAuth } from '../context/AuthContext.jsx';

/**
 * Protected Dashboard View.
 * 
 * @returns {React.JSX.Element} The Dashboard component.
 */
export const Dashboard = () => {
  const { currentUser, logout, authenticating } = useAuth();

  return (
    <div 
      className="dashboard-page" 
      style={{
        minHeight: '100vh',
        backgroundColor: '#0b0f19',
        color: '#f3f4f6',
        fontFamily: 'system-ui, -apple-system, sans-serif',
        padding: '2rem'
      }}
    >
      <div 
        style={{
          maxWidth: '1000px',
          margin: '0 auto',
          backgroundColor: 'rgba(255, 255, 255, 0.03)',
          border: '1px solid rgba(255, 255, 255, 0.05)',
          borderRadius: '1rem',
          padding: '2rem',
          backdropFilter: 'blur(20px)'
        }}
      >
        {/* Top Navigation Panel */}
        <div 
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            borderBottom: '1px solid rgba(255, 255, 255, 0.1)',
            paddingBottom: '1rem',
            marginBottom: '2rem'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <span style={{ fontSize: '1.75rem' }}>🚗</span>
            <h1 style={{ fontSize: '1.5rem', margin: 0, fontWeight: 700 }}>SmartRoad <span style={{ color: '#3b82f6' }}>Dashboard</span></h1>
          </div>
          
          <button
            onClick={logout}
            disabled={authenticating}
            style={{
              padding: '0.5rem 1.25rem',
              borderRadius: '0.5rem',
              border: '1px solid rgba(239, 68, 68, 0.3)',
              backgroundColor: 'transparent',
              color: '#ef4444',
              cursor: 'pointer',
              fontWeight: 600,
              transition: 'background-color 0.2s'
            }}
            onMouseOver={(e) => e.currentTarget.style.backgroundColor = 'rgba(239, 68, 68, 0.1)'}
            onMouseOut={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
          >
            {authenticating ? 'Signing Out...' : 'Log Out'}
          </button>
        </div>

        {/* User Card */}
        <div style={{ marginBottom: '2rem' }}>
          <h2>Welcome back, <span style={{ color: '#3b82f6' }}>{currentUser?.name || currentUser?.email || 'User'}</span>!</h2>
          <p style={{ opacity: 0.7, fontSize: '0.95rem' }}>Your active telemetry session is currently authenticated securely.</p>
        </div>

        {/* Telemetry Statistics Grid */}
        <div 
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
            gap: '1.5rem'
          }}
        >
          {[
            { title: 'System Status', value: 'Operational', icon: '🟢' },
            { title: 'Road Safety Score', value: '98 / 100', icon: '🛡️' },
            { title: 'Active Sensors', value: '4 Online', icon: '📡' },
            { title: 'Network Latency', value: '24 ms', icon: '⚡' }
          ].map((item, idx) => (
            <div 
              key={idx}
              style={{
                backgroundColor: 'rgba(255, 255, 255, 0.02)',
                border: '1px solid rgba(255, 255, 255, 0.05)',
                borderRadius: '0.75rem',
                padding: '1.25rem',
                display: 'flex',
                alignItems: 'center',
                gap: '1rem'
              }}
            >
              <span style={{ fontSize: '2rem' }}>{item.icon}</span>
              <div>
                <p style={{ margin: 0, fontSize: '0.8rem', opacity: 0.6 }}>{item.title}</p>
                <p style={{ margin: '0.25rem 0 0 0', fontSize: '1.25rem', fontWeight: 600 }}>{item.value}</p>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;