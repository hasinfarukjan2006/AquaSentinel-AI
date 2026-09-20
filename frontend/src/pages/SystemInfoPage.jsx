import React from 'react';
import { Info, Server, Cpu, Database, Activity, CheckCircle2 } from 'lucide-react';

export default function SystemInfoPage() {
  const systemStatus = [
    { name: 'Data Pipeline', status: 'Operational', icon: Activity, color: 'text-emerald-600', detail: 'Scripts 01-06 pipeline ready' },
    { name: 'ML Model Engine', status: 'Available', icon: Cpu, color: 'text-blue-600', detail: 'Random Forest & Isolation Forest joblib models' },
    { name: 'SQLite Database', status: 'Connected', icon: Database, color: 'text-emerald-600', detail: 'jalrakshak.db indexed tables' },
    { name: 'Last Processing Run', status: '2026-09-20', icon: CheckCircle2, color: 'text-indigo-600', detail: 'Processed 713 real & 520 synthetic records' },
    { name: 'Source Coverage', status: 'Multi-Source Integrated', icon: Server, color: 'text-slate-800', detail: 'CGWB (2024), IMD (1901-2021), Rajya Sabha (AU 557)' },
    { name: 'Model Validation', status: 'Prototype Decision-Support', icon: Info, color: 'text-amber-600', detail: 'Decision-support early warning platform' },
  ];

  return (
    <div className="space-y-6">
      
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
        <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
          <Info className="w-6 h-6 text-blue-600" />
          <span>System Information & Environment Diagnostics</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Technical specifications, architecture components, and subsystem health status
        </p>
      </div>

      {/* System Status Panel */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {systemStatus.map((item, i) => {
          const Icon = item.icon;
          return (
            <div key={i} className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-500 uppercase">{item.name}</span>
                <Icon className={`w-5 h-5 ${item.color}`} />
              </div>
              <div className={`text-lg font-bold ${item.color}`}>{item.status}</div>
              <p className="text-xs text-slate-400">{item.detail}</p>
            </div>
          );
        })}
      </div>

      {/* Architecture Overview */}
      <div className="bg-white p-6 rounded-xl border border-slate-200 shadow-xs space-y-4">
        <h2 className="text-base font-bold text-slate-900">Software Product Architecture</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
          
          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
            <h3 className="font-bold text-slate-900 text-sm">Frontend Layer</h3>
            <p className="text-slate-600">Vite + React.js + Tailwind CSS + Recharts + Leaflet Map Component</p>
            <p className="text-slate-400 font-mono">Port: 5173</p>
          </div>

          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
            <h3 className="font-bold text-slate-900 text-sm">Backend Layer</h3>
            <p className="text-slate-600">Python Flask REST API + SQLite (jalrakshak.db) + CORS Support</p>
            <p className="text-slate-400 font-mono">Port: 5000</p>
          </div>

          <div className="p-4 bg-slate-50 rounded-lg border border-slate-200 space-y-2">
            <h3 className="font-bold text-slate-900 text-sm">Data & ML Pipeline</h3>
            <p className="text-slate-600">Pandas Data Engineering + Scikit-Learn (Random Forest, Isolation Forest)</p>
            <p className="text-slate-400 font-mono">/ml/models/joblib</p>
          </div>

        </div>
      </div>

    </div>
  );
}
