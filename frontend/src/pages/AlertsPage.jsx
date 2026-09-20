import React, { useEffect, useState } from 'react';
import { Bell, AlertTriangle, ShieldAlert, CheckCircle2 } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';
import { fetchAlerts } from '../services/api';

export default function AlertsPage({ dataType, onSelectLocation }) {
  const [alerts, setAlerts] = useState([]);
  const [levelFilter, setLevelFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadAlerts() {
      setLoading(true);
      try {
        const res = await fetchAlerts(dataType, levelFilter);
        setAlerts(res.alerts || []);
      } catch (err) {
        console.error("Error fetching alerts:", err);
      } finally {
        setLoading(false);
      }
    }
    loadAlerts();
  }, [dataType, levelFilter]);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
            <Bell className="w-6 h-6 text-blue-600" />
            <span>Prototype Alert & Decision-Support Registry</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Automated early-warning triggers based on multi-indicator risk thresholds
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <span className="text-slate-500 font-medium">Filter Severity:</span>
          <select
            value={levelFilter}
            onChange={(e) => setLevelFilter(e.target.value)}
            className="px-3 py-1.5 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-slate-50 font-medium text-slate-700"
          >
            <option value="">All Alert Levels</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="VERY HIGH">VERY HIGH</option>
            <option value="HIGH">HIGH</option>
            <option value="MODERATE">MODERATE</option>
            <option value="LOW">LOW</option>
          </select>
        </div>
      </div>

      {/* Alert Cards List */}
      <div className="space-y-4">
        {alerts.length === 0 ? (
          <div className="bg-white p-8 rounded-xl border border-slate-200 text-center text-slate-500 text-sm">
            No active alerts matching current filter level.
          </div>
        ) : (
          alerts.map((alt, i) => (
            <div key={i} className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
              <div className="flex items-start justify-between">
                <div className="space-y-1">
                  <div className="flex items-center space-x-2">
                    <h3 className="font-bold text-slate-900 text-base">{alt.title}</h3>
                    <RiskBadge riskClass={alt.alert_level} score={alt.risk_score} />
                  </div>
                  <p className="text-xs text-slate-500">
                    Location: <strong>{alt.district}, {alt.state}</strong> • Created: {alt.created_at}
                  </p>
                </div>

                <button
                  onClick={() => onSelectLocation(alt.district)}
                  className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold px-3 py-1.5 rounded-lg shadow-xs"
                >
                  Verify District Profile
                </button>
              </div>

              <div className="p-3 bg-slate-50 rounded-lg border border-slate-200 text-xs text-slate-700 space-y-1">
                <div className="font-semibold text-slate-900">Trigger Reason:</div>
                <p className="leading-snug">{alt.reason}</p>
              </div>

              <div className="p-3 bg-blue-50 rounded-lg border border-blue-200 text-xs text-blue-900 flex items-start space-x-2">
                <CheckCircle2 className="w-4 h-4 text-blue-600 shrink-0 mt-0.5" />
                <div>
                  <span className="font-bold">Recommended Verification Action:</span>
                  <p className="mt-0.5 text-blue-800">{alt.recommended_action}</p>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

    </div>
  );
}
