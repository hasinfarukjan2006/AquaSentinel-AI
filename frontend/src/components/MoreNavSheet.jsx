import React from 'react';
import { 
  X, Activity, CloudRain, MapPin, Table, Cpu, CheckCircle2, Info 
} from 'lucide-react';

export default function MoreNavSheet({ isOpen, onClose, activeTab, setActiveTab }) {
  if (!isOpen) return null;

  const extraItems = [
    { id: 'health_trends', label: 'Health Trends', icon: Activity, desc: 'Rajya Sabha & Ministry reported cases' },
    { id: 'rainfall', label: 'Rainfall Trends', icon: CloudRain, desc: 'IMD Monsoon series & Z-scores' },
    { id: 'locations', label: 'Locations Directory', icon: MapPin, desc: 'District coordinates & profiles' },
    { id: 'data_explorer', label: 'Data Explorer', icon: Table, desc: 'Searchable audit table & CSV export' },
    { id: 'model_status', label: 'Model Status & ML', icon: Cpu, desc: 'Random Forest & Isolation Forest metrics' },
    { id: 'data_quality', label: 'Data Quality Audit', icon: CheckCircle2, desc: 'Data completeness & profiling' },
    { id: 'system_info', label: 'System Information', icon: Info, desc: 'Architecture & environment status' },
  ];

  return (
    <div className="fixed inset-0 z-50 flex flex-col justify-end bg-slate-950/70 backdrop-blur-xs transition-opacity lg:hidden">
      {/* Backdrop click to close */}
      <div className="flex-1" onClick={onClose} />

      {/* Sheet Content */}
      <div className="bg-slate-900 border-t border-slate-800 rounded-t-2xl p-4 space-y-4 max-h-[80vh] overflow-y-auto shadow-2xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center space-x-2">
            <span className="w-8 h-1 bg-slate-700 rounded-full mx-auto block mb-1"></span>
            <h3 className="font-bold text-white text-base">Additional Modules</h3>
          </div>
          <button
            onClick={onClose}
            className="p-2 text-slate-400 hover:text-white rounded-full bg-slate-800"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        <div className="space-y-2">
          {extraItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeTab === item.id;
            return (
              <button
                key={item.id}
                onClick={() => {
                  setActiveTab(item.id);
                  onClose();
                }}
                className={`w-full flex items-center space-x-3.5 p-3 rounded-xl text-left transition-colors min-h-[48px] ${
                  isActive
                    ? 'bg-blue-600 text-white font-bold shadow-xs'
                    : 'bg-slate-800/60 text-slate-300 hover:bg-slate-800'
                }`}
              >
                <Icon className={`w-5 h-5 shrink-0 ${isActive ? 'text-white' : 'text-blue-400'}`} />
                <div>
                  <div className="text-sm font-semibold">{item.label}</div>
                  <div className="text-[11px] text-slate-400 leading-tight">{item.desc}</div>
                </div>
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
}
