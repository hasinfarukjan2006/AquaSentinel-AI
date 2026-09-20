import React from 'react';
import { LayoutDashboard, ShieldAlert, Droplet, Bell, Menu } from 'lucide-react';

export default function BottomNav({ activeTab, setActiveTab, onOpenMore }) {
  const mainTabs = [
    { id: 'dashboard', label: 'Home', icon: LayoutDashboard },
    { id: 'risk_monitoring', label: 'Risk', icon: ShieldAlert },
    { id: 'water_quality', label: 'Water', icon: Droplet },
    { id: 'alerts', label: 'Alerts', icon: Bell },
  ];

  return (
    <nav aria-label="Mobile Navigation" className="lg:hidden fixed bottom-0 left-0 right-0 bg-slate-900 border-t border-slate-800 z-50 shadow-lg px-2 py-1 flex items-center justify-around">
      {mainTabs.map((tab) => {
        const Icon = tab.icon;
        const isActive = activeTab === tab.id;
        return (
          <button
            key={tab.id}
            onClick={() => setActiveTab(tab.id)}
            className={`flex flex-col items-center justify-center py-1.5 px-3 min-w-[56px] min-h-[44px] rounded-lg transition-colors ${
              isActive ? 'text-blue-400 font-bold' : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Icon className={`w-5 h-5 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
            <span className="text-[10px] mt-0.5 tracking-tight">{tab.label}</span>
          </button>
        );
      })}

      {/* More Button */}
      <button
        onClick={onOpenMore}
        className={`flex flex-col items-center justify-center py-1.5 px-3 min-w-[56px] min-h-[44px] rounded-lg transition-colors ${
          ['health_trends', 'rainfall', 'locations', 'data_explorer', 'model_status', 'data_quality', 'system_info'].includes(activeTab)
            ? 'text-blue-400 font-bold'
            : 'text-slate-400 hover:text-slate-200'
        }`}
      >
        <Menu className="w-5 h-5 text-slate-400" />
        <span className="text-[10px] mt-0.5 tracking-tight">More</span>
      </button>
    </nav>
  );
}
