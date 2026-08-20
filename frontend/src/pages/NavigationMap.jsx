import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { ROUTE_PATHS } from '../constants/routes.constants.js';

export const NavigationMap = () => {
  const [destination, setDestination] = useState('');
  const [searchQuery, setSearchQuery] = useState('');
  const [activeCategory, setActiveCategory] = useState('ALL');

  const emergencyLocations = [
    { id: 1, name: 'City Emergency Care Hospital', type: 'HOSPITAL', distance: '1.8 km', eta: '4 mins', lat: 16.5120, lon: 80.6510, phone: '+91 98765 43210' },
    { id: 2, name: 'Central Highway Police Station', type: 'POLICE', distance: '2.5 km', eta: '6 mins', lat: 16.5010, lon: 80.6410, phone: '112 / +91 91234 56789' },
    { id: 3, name: 'Metro Trauma Center', type: 'HOSPITAL', distance: '4.1 km', eta: '9 mins', lat: 16.5200, lon: 80.6620, phone: '+91 98765 11111' },
    { id: 4, name: 'Accident Hotspot - Bypass Junction', type: 'HOTSPOT', distance: '3.2 km', riskLevel: 'HIGH_RISK_ZONE', incidents: 14 }
  ];

  const filteredLocations = emergencyLocations.filter(loc => {
    if (activeCategory !== 'ALL' && loc.type !== activeCategory) return false;
    if (searchQuery && !loc.name.toLowerCase().includes(searchQuery.toLowerCase())) return false;
    return true;
  });

  return (
    <div style={{ minHeight: '100vh', backgroundColor: '#0b0f19', color: '#f3f4f6', fontFamily: 'system-ui, -apple-system, sans-serif', padding: '1.75rem' }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
        
        {/* Header */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', borderBottom: '1px solid rgba(255,255,255,0.1)', paddingBottom: '1rem' }}>
          <div>
            <h1 style={{ fontSize: '1.5rem', margin: 0, fontWeight: 700 }}>
              SmartRoad <span style={{ color: '#06b6d4' }}>Emergency Navigation & Map</span>
            </h1>
            <p style={{ margin: '0.25rem 0 0 0', opacity: 0.75, fontSize: '0.85rem' }}>
              Real-Time Route Guidance • Nearby Emergency Facilities • Spatial Accident Hotspots
            </p>
          </div>
          
          <div style={{ display: 'flex', gap: '0.75rem', alignItems: 'center' }}>
            <Link to={ROUTE_PATHS.DASHBOARD} style={{ padding: '0.45rem 1rem', borderRadius: '0.5rem', border: '1px solid rgba(6,182,212,0.4)', backgroundColor: 'rgba(6,182,212,0.1)', color: '#06b6d4', fontWeight: 600, textDecoration: 'none', fontSize: '0.85rem' }}>
              📊 Back to Dashboard
            </Link>
            <span style={{ fontSize: '0.8rem', fontWeight: 700, padding: '0.25rem 0.65rem', borderRadius: '0.375rem', backgroundColor: 'rgba(245,158,11,0.1)', color: '#f59e0b' }}>
              📍 GPS OFFLINE (HARDWARE DISCONNECTED)
            </span>
          </div>
        </div>

        {/* Top Control Bar */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', backgroundColor: 'rgba(255,255,255,0.025)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '0.75rem', padding: '0.85rem 1.25rem', marginBottom: '1.5rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            {['ALL', 'HOSPITAL', 'POLICE', 'HOTSPOT'].map(cat => (
              <button
                key={cat}
                onClick={() => setActiveCategory(cat)}
                style={{
                  padding: '0.35rem 0.85rem',
                  borderRadius: '0.5rem',
                  border: activeCategory === cat ? '1px solid #06b6d4' : '1px solid rgba(255,255,255,0.1)',
                  backgroundColor: activeCategory === cat ? 'rgba(6,182,212,0.15)' : 'transparent',
                  color: activeCategory === cat ? '#06b6d4' : '#9ca3af',
                  fontSize: '0.8rem',
                  fontWeight: 700,
                  cursor: 'pointer'
                }}
              >
                {cat === 'ALL' ? '🌐 All Locations' : (cat === 'HOSPITAL' ? '🏥 Hospitals' : (cat === 'POLICE' ? '🚓 Police Stations' : '⚠️ Hotspots'))}
              </button>
            ))}
          </div>

          <div style={{ display: 'flex', gap: '0.5rem', width: '320px' }}>
            <input
              type="text"
              placeholder="Search emergency locations..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              style={{ width: '100%', padding: '0.4rem 0.75rem', borderRadius: '0.5rem', border: '1px solid rgba(255,255,255,0.1)', backgroundColor: 'rgba(0,0,0,0.4)', color: '#fff', fontSize: '0.85rem' }}
            />
          </div>
        </div>

        {/* Map Grid */}
        <div style={{ display: 'grid', gridTemplateColumns: '2fr 1fr', gap: '1.5rem' }}>
          
          {/* Interactive Map Visual Mock Canvas */}
          <div style={{ backgroundColor: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '1rem', padding: '1.25rem', position: 'relative', minHeight: '480px', display: 'flex', flexDirection: 'column' }}>
            <div style={{ position: 'absolute', top: '20px', left: '20px', backgroundColor: 'rgba(11,15,25,0.85)', padding: '0.5rem 0.85rem', borderRadius: '0.5rem', border: '1px solid rgba(6,182,212,0.3)', fontSize: '0.8rem', zIndex: 10 }}>
              <span style={{ color: '#06b6d4', fontWeight: 700 }}>📍 CURRENT POSITION:</span> Vijayawada Corridor (16.5062 N, 80.6480 E)
            </div>

            {/* Map Grid SVG Simulation Background */}
            <div style={{ flex: 1, backgroundColor: '#070a12', borderRadius: '0.75rem', overflow: 'hidden', border: '1px solid rgba(6,182,212,0.15)', display: 'flex', alignItems: 'center', justifyContent: 'center', position: 'relative' }}>
              <svg width="100%" height="100%" style={{ position: 'absolute', top: 0, left: 0, opacity: 0.15 }}>
                <defs>
                  <pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
                    <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#06b6d4" strokeWidth="1"/>
                  </pattern>
                </defs>
                <rect width="100%" height="100%" fill="url(#grid)" />
              </svg>

              {/* Highway Route Path Line */}
              <svg width="100%" height="100%" style={{ position: 'absolute', top: 0, left: 0 }}>
                <path d="M 100 350 Q 250 150 500 220 T 700 100" fill="none" stroke="#06b6d4" strokeWidth="4" strokeDasharray="8 4" />
              </svg>

              {/* Location Pins */}
              <div style={{ position: 'absolute', top: '45%', left: '30%', cursor: 'pointer', textAlign: 'center' }}>
                <span style={{ fontSize: '1.75rem' }}>🚗</span>
                <div style={{ backgroundColor: '#06b6d4', color: '#000', fontSize: '0.65rem', fontWeight: 800, padding: '2px 6px', borderRadius: '4px' }}>YOUR CAR</div>
              </div>

              <div style={{ position: 'absolute', top: '25%', left: '55%', cursor: 'pointer', textAlign: 'center' }}>
                <span style={{ fontSize: '1.75rem' }}>🏥</span>
                <div style={{ backgroundColor: '#10b981', color: '#000', fontSize: '0.65rem', fontWeight: 800, padding: '2px 6px', borderRadius: '4px' }}>CITY HOSPITAL</div>
              </div>

              <div style={{ position: 'absolute', top: '65%', left: '70%', cursor: 'pointer', textAlign: 'center' }}>
                <span style={{ fontSize: '1.75rem' }}>🚓</span>
                <div style={{ backgroundColor: '#3b82f6', color: '#fff', fontSize: '0.65rem', fontWeight: 800, padding: '2px 6px', borderRadius: '4px' }}>POLICE HQ</div>
              </div>

              <div style={{ position: 'absolute', top: '20%', left: '80%', cursor: 'pointer', textAlign: 'center' }}>
                <span style={{ fontSize: '1.75rem' }}>⚠️</span>
                <div style={{ backgroundColor: '#ef4444', color: '#fff', fontSize: '0.65rem', fontWeight: 800, padding: '2px 6px', borderRadius: '4px' }}>ACCIDENT HOTSPOT</div>
              </div>
            </div>
          </div>

          {/* Location List Panel */}
          <div style={{ backgroundColor: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.08)', borderRadius: '1rem', padding: '1.25rem', display: 'flex', flexDirection: 'column' }}>
            <h3 style={{ margin: '0 0 1rem 0', fontSize: '1rem', fontWeight: 600 }}>🏥 Nearby Emergency Facilities</h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem', overflowY: 'auto' }}>
              {filteredLocations.map((loc) => (
                <div key={loc.id} style={{ padding: '0.85rem', backgroundColor: 'rgba(255,255,255,0.02)', border: '1px solid rgba(255,255,255,0.05)', borderRadius: '0.75rem' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline' }}>
                    <span style={{ fontWeight: 700, fontSize: '0.85rem' }}>
                      {loc.type === 'HOSPITAL' ? '🏥' : (loc.type === 'POLICE' ? '🚓' : '⚠️')} {loc.name}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: '#06b6d4', fontWeight: 700 }}>{loc.distance}</span>
                  </div>
                  
                  {loc.eta && <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.75rem', opacity: 0.7 }}>Est. Emergency Drive: <strong>{loc.eta}</strong></p>}
                  {loc.phone && <p style={{ margin: '0.15rem 0 0 0', fontSize: '0.75rem', color: '#10b981', fontFamily: 'monospace' }}>Phone: {loc.phone}</p>}
                  {loc.incidents && <p style={{ margin: '0.15rem 0 0 0', fontSize: '0.75rem', color: '#ef4444' }}>High Risk Zone ({loc.incidents} incidents)</p>}
                </div>
              ))}
            </div>
          </div>

        </div>

      </div>
    </div>
  );
};

export default NavigationMap;
