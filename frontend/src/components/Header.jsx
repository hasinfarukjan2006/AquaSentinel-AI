import React from 'react';
import { Droplets, Activity, Database, UserCheck } from 'lucide-react';

export default function Header({ dataType, setDataType, userRole, setUserRole }) {
  return (
    <header className="bg-slate-900 text-white border-b border-slate-800 sticky top-0 z-40">
      <div className="max-w-7xl mx-auto px-3 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-14 sm:h-16">
          
          {/* Logo & Title */}
          <div className="flex items-center space-x-2.5">
            <div className="p-1.5 sm:p-2 bg-blue-600 rounded-lg text-white shadow-md">
              <Droplets className="w-5 h-5 sm:w-6 sm:h-6" />
            </div>
            <div>
              <div className="flex items-center space-x-1.5">
                <span className="text-base sm:text-xl font-bold tracking-tight text-white">AquaSentinel</span>
                <span className="text-[10px] sm:text-xs bg-blue-900 text-blue-200 px-1.5 py-0.5 rounded border border-blue-700 font-mono">
                  PWA
                </span>
              </div>
              <p className="text-[10px] sm:text-xs text-slate-400 font-medium hidden sm:block">
                Community Water-Borne Disease Early Warning System
              </p>
            </div>
          </div>

          {/* Controls: Mode Switcher & Role Selector */}
          <div className="flex items-center space-x-2 sm:space-x-4">
            
            {/* Mode Toggle */}
            <div className="flex items-center bg-slate-800 p-0.5 sm:p-1 rounded-lg border border-slate-700 text-[11px] sm:text-xs">
              <button
                onClick={() => setDataType('SYNTHETIC_DEMO')}
                className={`px-2 py-1 sm:px-3 sm:py-1.5 rounded-md font-medium transition-colors flex items-center space-x-1 min-h-[36px] ${
                  dataType === 'SYNTHETIC_DEMO'
                    ? 'bg-blue-600 text-white shadow-xs'
                    : 'text-slate-400 hover:text-white'
                }`}
                title="Full multi-indicator demo mode"
              >
                <Activity className="w-3.5 h-3.5" />
                <span>Demo</span>
              </button>
              <button
                onClick={() => setDataType('REAL_PUBLIC_SOURCE')}
                className={`px-2 py-1 sm:px-3 sm:py-1.5 rounded-md font-medium transition-colors flex items-center space-x-1 min-h-[36px] ${
                  dataType === 'REAL_PUBLIC_SOURCE'
                    ? 'bg-emerald-600 text-white shadow-xs'
                    : 'text-slate-400 hover:text-white'
                }`}
                title="Strict real public source datasets"
              >
                <Database className="w-3.5 h-3.5" />
                <span>Real</span>
              </button>
            </div>

            {/* Role Selector (hidden on smallest screens, visible sm+) */}
            <div className="hidden sm:flex items-center space-x-1.5 text-xs bg-slate-800 px-2.5 py-1.5 rounded-lg border border-slate-700 min-h-[36px]">
              <UserCheck className="w-4 h-4 text-blue-400" />
              <select
                value={userRole}
                onChange={(e) => setUserRole(e.target.value)}
                className="bg-transparent text-white focus:outline-none cursor-pointer font-medium"
              >
                <option value="HEALTH_OFFICIAL" className="bg-slate-900">Health Official</option>
                <option value="ADMIN" className="bg-slate-900">Admin</option>
                <option value="FIELD_WORKER" className="bg-slate-900">Field Worker</option>
                <option value="VIEWER" className="bg-slate-900">Viewer</option>
              </select>
            </div>

          </div>

        </div>
      </div>
    </header>
  );
}
