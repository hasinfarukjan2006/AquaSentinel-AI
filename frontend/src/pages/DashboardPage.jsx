import React, { useEffect, useState } from 'react';
import { 
  ShieldAlert, Activity, Droplets, CloudRain, AlertTriangle, 
  MapPin, CheckCircle2, Database, ArrowUpRight, TrendingUp, Layers
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, 
  Cell
} from 'recharts';
import RiskBadge from '../components/RiskBadge';
import RiskMap from '../components/RiskMap';
import { fetchSummary, fetchLocations, fetchAlerts, fetchRainfall } from '../services/api';

export default function DashboardPage({ dataType, onSelectLocation }) {
  const [summary, setSummary] = useState(null);
  const [locations, setLocations] = useState([]);
  const [alerts, setAlerts] = useState([]);
  const [rainfallData, setRainfallData] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDashboardData() {
      setLoading(true);
      try {
        const sumRes = await fetchSummary(dataType);
        const locRes = await fetchLocations(dataType);
        const altRes = await fetchAlerts(dataType);
        const rfRes = await fetchRainfall(dataType);

        setSummary(sumRes);
        setLocations(locRes.locations || []);
        setAlerts(altRes.alerts || []);
        setRainfallData(rfRes.records || []);
      } catch (err) {
        console.error("Error loading dashboard data:", err);
      } finally {
        setLoading(false);
      }
    }
    loadDashboardData();
  }, [dataType]);

  if (loading || !summary) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-500">
        <Activity className="w-6 h-6 animate-spin mr-2 text-blue-600" />
        <span className="text-sm">Loading AquaSentinel Mobile Dashboard...</span>
      </div>
    );
  }

  const distData = Object.entries(summary.risk_distribution || {}).map(([key, val]) => ({
    name: key,
    value: val
  }));

  const COLORS = {
    LOW: '#10b981',
    MODERATE: '#f59e0b',
    HIGH: '#f97316',
    'VERY HIGH': '#ef4444',
    CRITICAL: '#8b5cf6'
  };

  const topHighRisk = (summary.high_risk_locations || [])[0] || {
    district: 'Salem',
    risk_score: 72,
    risk_class: 'VERY HIGH'
  };

  return (
    <div className="space-y-4 sm:space-y-6 pb-16 lg:pb-0">
      
      {/* Mobile Top Header */}
      <div className="bg-slate-900 text-white p-4 sm:p-5 rounded-xl border border-slate-800 space-y-2 shadow-sm">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <Droplets className="w-5 h-5 text-blue-400 shrink-0" />
            <h1 className="text-lg sm:text-xl font-bold">AquaSentinel</h1>
          </div>
          <span className="text-[10px] sm:text-xs bg-blue-500/20 text-blue-300 border border-blue-400/30 px-2 py-0.5 rounded font-mono">
            {dataType}
          </span>
        </div>
        <p className="text-xs text-slate-400">
          Community Water-Borne Disease Early Warning System
        </p>
      </div>

      {/* Primary Mobile Risk Hero Card */}
      <div className="bg-slate-900 text-white p-5 rounded-xl border border-slate-800 space-y-4 shadow-md">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
            Highest Monitored Location Signal
          </span>
          <RiskBadge riskClass={topHighRisk.risk_class} />
        </div>

        <div className="flex items-center justify-between">
          <div>
            <div className="text-xl sm:text-2xl font-extrabold text-white">{topHighRisk.district}</div>
            <div className="text-xs text-slate-400">Risk Indicator Score</div>
          </div>

          <div className="text-right">
            <div className="text-3xl sm:text-4xl font-black text-white">{topHighRisk.risk_score} <span className="text-xs text-slate-400 font-normal">/ 100</span></div>
          </div>
        </div>

        <div className="p-3 bg-blue-950/60 border border-blue-800/60 rounded-lg text-xs text-blue-200 flex items-start space-x-2">
          <CheckCircle2 className="w-4 h-4 text-blue-400 shrink-0 mt-0.5" />
          <span>Verification recommended: Check local ground water and symptom reports.</span>
        </div>
      </div>

      {/* 3 Mobile Signal Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
        
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div className="space-y-0.5">
            <span className="text-[11px] font-semibold text-slate-500 uppercase">Health Signal</span>
            <div className="text-sm font-bold text-slate-900">Elevated Symptoms</div>
          </div>
          <Activity className="w-5 h-5 text-amber-500 shrink-0" />
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div className="space-y-0.5">
            <span className="text-[11px] font-semibold text-slate-500 uppercase">Water Signal</span>
            <div className="text-sm font-bold text-slate-900">IS 10500 Deviation</div>
          </div>
          <Droplets className="w-5 h-5 text-rose-500 shrink-0" />
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex items-center justify-between">
          <div className="space-y-0.5">
            <span className="text-[11px] font-semibold text-slate-500 uppercase">Rainfall Signal</span>
            <div className="text-sm font-bold text-slate-900">Monsoon Surplus</div>
          </div>
          <CloudRain className="w-5 h-5 text-blue-600 shrink-0" />
        </div>

      </div>

      {/* Interactive Map Section */}
      <div className="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
        <div className="flex items-center justify-between">
          <h2 className="text-sm sm:text-base font-bold text-slate-900 flex items-center space-x-2">
            <MapPin className="w-4 h-4 text-blue-600" />
            <span>Interactive Risk Map</span>
          </h2>
          <span className="text-[11px] text-slate-500">{locations.length} points</span>
        </div>
        <RiskMap locations={locations} onSelectLocation={onSelectLocation} />
      </div>

      {/* Risk Distribution Chart */}
      <div className="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
        <h2 className="text-sm sm:text-base font-bold text-slate-900 flex items-center space-x-2">
          <TrendingUp className="w-4 h-4 text-blue-600" />
          <span>Current Risk Distribution</span>
        </h2>
        <div className="h-48 sm:h-56">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={distData} layout="vertical" margin={{ top: 5, right: 15, left: 15, bottom: 5 }}>
              <XAxis type="number" />
              <YAxis dataKey="name" type="category" width={75} tick={{ fontSize: 10 }} />
              <Tooltip />
              <Bar dataKey="value" radius={[0, 4, 4, 0]}>
                {distData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={COLORS[entry.name] || '#64748b'} />
                ))}
              </Bar>
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Recent Alerts List (Mobile Cards) */}
      <div className="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-xs space-y-3">
        <div className="flex items-center justify-between border-b pb-2">
          <h2 className="text-sm sm:text-base font-bold text-slate-900 flex items-center space-x-2">
            <AlertTriangle className="w-4 h-4 text-amber-500" />
            <span>Recent Decision Alerts</span>
          </h2>
          <span className="text-[11px] text-slate-500">Early warnings</span>
        </div>

        <div className="space-y-3">
          {alerts.slice(0, 3).map((alt, i) => (
            <div key={i} className="p-3 bg-slate-50 rounded-xl border border-slate-200 space-y-2">
              <div className="flex items-center justify-between">
                <span className="font-bold text-xs text-slate-900">{alt.district}</span>
                <RiskBadge riskClass={alt.alert_level} score={alt.risk_score} />
              </div>
              <p className="text-[11px] text-slate-600 leading-snug">{alt.reason}</p>
              <button
                onClick={() => onSelectLocation(alt.district)}
                className="w-full bg-blue-600 hover:bg-blue-700 text-white text-[11px] font-semibold py-1.5 rounded-lg flex items-center justify-center space-x-1 min-h-[36px]"
              >
                <span>Inspect District Details</span>
                <ArrowUpRight className="w-3.5 h-3.5" />
              </button>
            </div>
          ))}
        </div>
      </div>

    </div>
  );
}
