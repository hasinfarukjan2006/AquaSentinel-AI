import React from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import L from 'leaflet';
import RiskBadge from './RiskBadge';

// Custom Leaflet Markers by Risk Level
const createCustomIcon = (color) => {
  return L.divIcon({
    className: 'custom-leaflet-marker',
    html: `<div style="background-color: ${color}; width: 14px; height: 14px; border-radius: 50%; border: 2px solid white; box-shadow: 0 0 6px rgba(0,0,0,0.4);"></div>`,
    iconSize: [14, 14],
    iconAnchor: [7, 7]
  });
};

const getMarkerColor = (riskClass) => {
  switch (riskClass) {
    case 'LOW': return '#10b981';
    case 'MODERATE': return '#f59e0b';
    case 'HIGH': return '#f97316';
    case 'VERY HIGH': return '#ef4444';
    case 'CRITICAL': return '#8b5cf6';
    default: return '#64748b';
  }
};

export default function RiskMap({ locations, onSelectLocation }) {
  // Center map around South/East India (Tamil Nadu/AP/Assam center)
  const defaultCenter = [15.5000, 79.5000];
  const defaultZoom = 6;

  const validLocations = locations.filter(
    (loc) => loc.latitude && loc.longitude && !isNaN(loc.latitude) && !isNaN(loc.longitude)
  );

  return (
    <div className="w-full h-96 rounded-xl overflow-hidden border border-slate-200 shadow-sm relative z-0">
      {validLocations.length === 0 ? (
        <div className="w-full h-full flex flex-col items-center justify-center bg-slate-100 text-slate-500 text-sm p-4">
          <p className="font-semibold">No geographic coordinates available in current view.</p>
          <p className="text-xs text-slate-400 mt-1">
            Displaying {validLocations.length} locations with valid coordinates out of {locations.length} total monitored locations.
          </p>
        </div>
      ) : (
        <MapContainer
          center={defaultCenter}
          zoom={defaultZoom}
          scrollWheelZoom={true}
          style={{ width: '100%', height: '100%' }}
        >
          <TileLayer
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
          />

          {validLocations.map((loc, idx) => (
            <Marker
              key={idx}
              position={[loc.latitude, loc.longitude]}
              icon={createCustomIcon(getMarkerColor(loc.latest_risk_class))}
            >
              <Popup>
                <div className="p-1 space-y-2 min-w-[180px]">
                  <div className="flex items-center justify-between border-b pb-1">
                    <span className="font-bold text-slate-900 text-sm">{loc.district}</span>
                    <span className="text-xs text-slate-500">{loc.state}</span>
                  </div>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-slate-600">Risk Indicator:</span>
                    <RiskBadge riskClass={loc.latest_risk_class} score={loc.latest_risk_score} />
                  </div>
                  <button
                    onClick={() => onSelectLocation(loc.district)}
                    className="w-full mt-2 bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold py-1 rounded shadow-xs"
                  >
                    View Location Details
                  </button>
                </div>
              </Popup>
            </Marker>
          ))}
        </MapContainer>
      )}
    </div>
  );
}
