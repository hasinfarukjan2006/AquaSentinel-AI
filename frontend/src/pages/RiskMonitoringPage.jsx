import React, { useEffect, useState } from 'react';
import { ShieldAlert, Search, ArrowUpRight, Activity } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';
import { fetchRiskRecords } from '../services/api';

export default function RiskMonitoringPage({ dataType, onSelectLocation }) {
  const [records, setRecords] = useState([]);
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadRiskData() {
      setLoading(true);
      try {
        const res = await fetchRiskRecords(dataType, { limit: 200 });
        setRecords(res.records || []);
      } catch (err) {
        console.error("Error fetching risk records:", err);
      } finally {
        setLoading(false);
      }
    }
    loadRiskData();
  }, [dataType]);

  const filteredRecords = records.filter(r => {
    const matchesSearch = !search || 
      (r.district && r.district.toLowerCase().includes(search.toLowerCase())) ||
      (r.state && r.state.toLowerCase().includes(search.toLowerCase()));
    const matchesRisk = !riskFilter || r.risk_class === riskFilter;
    return matchesSearch && matchesRisk;
  });

  return (
    <div className="space-y-4 sm:space-y-6 pb-16 lg:pb-0">
      
      {/* Header & Controls */}
      <div className="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <h1 className="text-lg sm:text-xl font-bold text-slate-900 flex items-center space-x-2">
            <ShieldAlert className="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" />
            <span>Risk Monitoring Registry</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Community risk indicators ($R = 100(0.25S + 0.25W + 0.20E + 0.15H + 0.10V + 0.05A)$)
          </p>
        </div>

        {/* Filters */}
        <div className="flex flex-col sm:flex-row items-stretch sm:items-center gap-2 text-xs">
          <div className="relative">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search district or state..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              className="pl-9 pr-4 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-slate-50 w-full sm:w-56 min-h-[40px]"
            />
          </div>

          <select
            value={riskFilter}
            onChange={(e) => setRiskFilter(e.target.value)}
            className="px-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-slate-50 text-slate-700 font-medium min-h-[40px]"
          >
            <option value="">All Risk Bands</option>
            <option value="CRITICAL">CRITICAL</option>
            <option value="VERY HIGH">VERY HIGH</option>
            <option value="HIGH">HIGH</option>
            <option value="MODERATE">MODERATE</option>
            <option value="LOW">LOW</option>
          </select>
        </div>
      </div>

      {loading ? (
        <div className="p-12 flex items-center justify-center text-slate-500 bg-white rounded-xl border border-slate-200">
          <Activity className="w-5 h-5 animate-spin mr-2 text-blue-600" />
          <span className="text-sm">Loading Risk Registry...</span>
        </div>
      ) : (
        <>
          {/* Mobile Stacked Cards (visible on mobile <768px) */}
          <div className="block md:hidden space-y-3">
            {filteredRecords.length === 0 ? (
              <div className="p-6 bg-white rounded-xl border border-slate-200 text-center text-xs text-slate-500">
                No risk records found matching filter criteria.
              </div>
            ) : (
              filteredRecords.map((r, i) => (
                <div key={i} className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-3">
                  <div className="flex items-start justify-between">
                    <div>
                      <h3 className="font-bold text-slate-900 text-base">{r.district}</h3>
                      <p className="text-xs text-slate-500">{r.state} ({r.season} {r.year})</p>
                    </div>
                    <RiskBadge riskClass={r.risk_class} score={r.risk_score} />
                  </div>

                  <div className="grid grid-cols-2 gap-2 text-[11px] bg-slate-50 p-2.5 rounded-lg border border-slate-100">
                    <div>
                      <span className="text-slate-400 block">Water Signal</span>
                      <span className="font-semibold text-slate-800">
                        {r.water_component > 0.4 ? 'Deviation Detected' : 'Normal Range'}
                      </span>
                    </div>
                    <div>
                      <span className="text-slate-400 block">Rainfall Signal</span>
                      <span className="font-semibold text-slate-800">
                        {r.env_component > 0.5 ? 'Monsoon Surplus' : 'Moderate'}
                      </span>
                    </div>
                  </div>

                  {r.abnormal_pattern_flag === 1 && (
                    <div className="text-[11px] font-semibold text-rose-700 bg-rose-50 border border-rose-200 p-1.5 rounded text-center">
                      Abnormal pattern detected
                    </div>
                  )}

                  <button
                    onClick={() => onSelectLocation(r.district)}
                    className="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2 rounded-lg text-xs flex items-center justify-center space-x-1 min-h-[44px] shadow-xs"
                  >
                    <span>Inspect District Profile</span>
                    <ArrowUpRight className="w-4 h-4" />
                  </button>
                </div>
              ))
            )}
          </div>

          {/* Desktop Table (visible on desktop >=768px) */}
          <div className="hidden md:block bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
            <div className="overflow-x-auto">
              <table className="w-full text-left text-xs text-slate-600">
                <thead className="bg-slate-100 text-slate-700 uppercase font-semibold border-b">
                  <tr>
                    <th className="py-3 px-4">Location</th>
                    <th className="py-3 px-4">Risk Indicator</th>
                    <th className="py-3 px-4">Health Signal</th>
                    <th className="py-3 px-4">Water Signal</th>
                    <th className="py-3 px-4">Rainfall Signal</th>
                    <th className="py-3 px-4">Anomaly Flag</th>
                    <th className="py-3 px-4">Data Availability</th>
                    <th className="py-3 px-4">Action</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100">
                  {filteredRecords.map((r, i) => (
                    <tr key={i} className="hover:bg-slate-50 transition-colors">
                      <td className="py-3 px-4">
                        <div className="font-bold text-slate-900 text-sm">{r.district}</div>
                        <div className="text-[11px] text-slate-500">{r.state} ({r.season} {r.year})</div>
                      </td>

                      <td className="py-3 px-4">
                        <RiskBadge riskClass={r.risk_class} score={r.risk_score} />
                      </td>

                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${
                          r.health_component > 0.4 ? 'bg-amber-100 text-amber-800' : 'bg-slate-100 text-slate-700'
                        }`}>
                          {r.health_component > 0.4 ? 'Elevated Signal' : 'Baseline'}
                        </span>
                      </td>

                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${
                          r.water_component > 0.4 ? 'bg-rose-100 text-rose-800' : 'bg-slate-100 text-slate-700'
                        }`}>
                          {r.water_component > 0.4 ? 'Deviation Detected' : 'Normal Range'}
                        </span>
                      </td>

                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded text-[11px] font-medium ${
                          r.env_component > 0.5 ? 'bg-orange-100 text-orange-800' : 'bg-slate-100 text-slate-700'
                        }`}>
                          {r.env_component > 0.5 ? 'Monsoon Surplus' : 'Moderate'}
                        </span>
                      </td>

                      <td className="py-3 px-4">
                        {r.abnormal_pattern_flag === 1 ? (
                          <span className="px-2 py-0.5 rounded text-[11px] font-semibold bg-rose-100 text-rose-700 border border-rose-200">
                            Abnormal pattern detected
                          </span>
                        ) : (
                          <span className="text-slate-400 text-[11px]">Normal Pattern</span>
                        )}
                      </td>

                      <td className="py-3 px-4 font-mono text-[11px] text-slate-500">
                        {r.data_availability_status}
                      </td>

                      <td className="py-3 px-4">
                        <button
                          onClick={() => onSelectLocation(r.district)}
                          className="bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 px-3 py-1.5 rounded text-xs font-semibold flex items-center space-x-1"
                        >
                          <span>Inspect</span>
                          <ArrowUpRight className="w-3.5 h-3.5" />
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}

    </div>
  );
}
