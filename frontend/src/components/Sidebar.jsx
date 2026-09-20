import React from 'react';
import { 
  LayoutDashboard, ShieldAlert, Droplet, CloudRain, Activity, 
  MapPin, Bell, Table, Cpu, CheckCircle2, Info, Lock
} from 'lucide-react';

export default function Sidebar({ activeTab, setActiveTab }) {
  const menuItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'risk_monitoring', label: 'Risk Monitoring', icon: ShieldAlert },
    { id: 'water_quality', label: 'Water Quality', icon: Droplet },
    { id: 'rainfall', label: 'Rainfall', icon: CloudRain },
    { id: 'health_trends', label: 'Health Trends', icon: Activity },
    { id: 'locations', label: 'Locations', icon: MapPin },
    { id: 'alerts', label: 'Alerts', icon: Bell },
    { id: 'data_explorer', label: 'Data Explorer', icon: Table },
    { id: 'model_status', label: 'Model Status', icon: Cpu },
    { id: 'data_quality', label: 'Data Quality', icon: CheckCircle2 },
    { id: 'system_info', label: 'System Information', icon: Info },
  ];

  return (
    <aside className="hidden lg:flex w-64 bg-slate-900 text-slate-300 min-h-screen border-r border-slate-800 flex-col justify-between shrink-0">
      <div className="p-4 space-y-1">
        <div className="px-3 py-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">
          Navigation
        </div>
        {menuItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white shadow-sm'
                  : 'text-slate-400 hover:bg-slate-800 hover:text-slate-200'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>

      <div className="p-4 border-t border-slate-800 bg-slate-950/50">
        <div className="flex items-center space-x-2 text-xs text-slate-500">
          <Lock className="w-3.5 h-3.5 text-slate-400" />
          <span>Decision-Support System</span>
        </div>
        <p className="text-[11px] text-slate-400 mt-1 leading-tight">
          Early-warning decision support platform. Not a diagnosis tool.
        </p>
      </div>
    </aside>
  );
}
