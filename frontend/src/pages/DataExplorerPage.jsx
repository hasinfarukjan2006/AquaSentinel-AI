import React, { useEffect, useState } from 'react';
import { Table, Search, Download, ChevronLeft, ChevronRight, Filter, X } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';
import { fetchRiskRecords } from '../services/api';

export default function DataExplorerPage({ dataType }) {
  const [records, setRecords] = useState([]);
  const [search, setSearch] = useState('');
  const [riskFilter, setRiskFilter] = useState('');
  const [isFilterModalOpen, setIsFilterModalOpen] = useState(false);
  const [currentPage, setCurrentPage] = useState(1);
  const pageSize = 20;

  useEffect(() => {
    async function loadData() {
      try {
        const res = await fetchRiskRecords(dataType, { limit: 500 });
        setRecords(res.records || []);
      } catch (err) {
        console.error("Error loading explorer records:", err);
      }
    }
    loadData();
  }, [dataType]);

  const filtered = records.filter(r => {
    const matchesSearch = !search || 
      (r.district && r.district.toLowerCase().includes(search.toLowerCase())) ||
      (r.state && r.state.toLowerCase().includes(search.toLowerCase())) ||
      (r.record_id && r.record_id.toLowerCase().includes(search.toLowerCase()));
    const matchesRisk = !riskFilter || r.risk_class === riskFilter;
    return matchesSearch && matchesRisk;
  });

  const totalPages = Math.ceil(filtered.length / pageSize) || 1;
  const paginated = filtered.slice((currentPage - 1) * pageSize, currentPage * pageSize);

  const handleExportCSV = () => {
    if (filtered.length === 0) return;
    const headers = Object.keys(filtered[0]).join(',');
    const rows = filtered.map(r => Object.values(r).map(v => `"${v !== null ? v : ''}"`).join(','));
    const csvContent = "data:text/csv;charset=utf-8," + [headers, ...rows].join("\n");
    const encodedUri = encodeURI(csvContent);
    const link = document.createElement("a");
    link.setAttribute("href", encodedUri);
    link.setAttribute("download", `AquaSentinel_Export_${dataType}.csv`);
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <div className="space-y-4 sm:space-y-6 pb-16 lg:pb-0">
      
      {/* Header & Controls */}
      <div className="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <h1 className="text-lg sm:text-xl font-bold text-slate-900 flex items-center space-x-2">
            <Table className="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" />
            <span>Data Explorer & Audit</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Search, filter, and export underlying integrated records ({filtered.length} total entries)
          </p>
        </div>

        <div className="flex items-center space-x-2 text-xs">
          <div className="relative flex-1 sm:flex-none">
            <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
            <input
              type="text"
              placeholder="Search ID, district, state..."
              value={search}
              onChange={(e) => { setSearch(e.target.value); setCurrentPage(1); }}
              className="pl-9 pr-3 py-2 border border-slate-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-slate-50 w-full sm:w-56 min-h-[40px]"
            />
          </div>

          {/* Mobile Filter Button */}
          <button
            onClick={() => setIsFilterModalOpen(true)}
            className="md:hidden bg-slate-100 hover:bg-slate-200 text-slate-700 font-semibold px-3 py-2 rounded-lg border border-slate-300 flex items-center space-x-1 min-h-[40px]"
          >
            <Filter className="w-4 h-4" />
            <span>Filter</span>
          </button>

          {/* Export Button */}
          <button
            onClick={handleExportCSV}
            className="bg-slate-900 hover:bg-slate-800 text-white font-semibold px-3 py-2 rounded-lg flex items-center space-x-1.5 shadow-xs min-h-[40px]"
          >
            <Download className="w-4 h-4" />
            <span className="hidden sm:inline">Export CSV</span>
          </button>
        </div>
      </div>

      {/* Mobile Filter Bottom Sheet Modal */}
      {isFilterModalOpen && (
        <div className="fixed inset-0 z-50 flex flex-col justify-end bg-slate-950/70 backdrop-blur-xs md:hidden">
          <div className="bg-white rounded-t-2xl p-5 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b pb-2">
              <h3 className="font-bold text-slate-900 text-base">Filter Explorer Records</h3>
              <button onClick={() => setIsFilterModalOpen(false)} className="p-1 text-slate-400 hover:text-slate-600">
                <X className="w-5 h-5" />
              </button>
            </div>
            
            <div>
              <label className="block text-xs font-semibold text-slate-700 uppercase mb-1">Filter by Risk Band</label>
              <select
                value={riskFilter}
                onChange={(e) => { setRiskFilter(e.target.value); setCurrentPage(1); }}
                className="w-full p-2.5 border border-slate-300 rounded-lg text-xs bg-slate-50 font-medium"
              >
                <option value="">All Risk Bands</option>
                <option value="CRITICAL">CRITICAL</option>
                <option value="VERY HIGH">VERY HIGH</option>
                <option value="HIGH">HIGH</option>
                <option value="MODERATE">MODERATE</option>
                <option value="LOW">LOW</option>
              </select>
            </div>

            <button
              onClick={() => setIsFilterModalOpen(false)}
              className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded-lg text-xs min-h-[44px]"
            >
              Apply Filter
            </button>
          </div>
        </div>
      )}

      {/* Mobile Stacked Cards (<768px) */}
      <div className="block md:hidden space-y-3">
        {paginated.map((r, i) => (
          <div key={i} className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-2.5">
            <div className="flex items-start justify-between">
              <div>
                <span className="font-mono text-[10px] text-slate-400 block">{r.record_id}</span>
                <h3 className="font-bold text-slate-900 text-base">{r.district}</h3>
                <p className="text-xs text-slate-500">{r.state} ({r.season} {r.year})</p>
              </div>
              <RiskBadge riskClass={r.risk_class} score={r.risk_score} />
            </div>

            <div className="grid grid-cols-2 gap-2 text-[11px] bg-slate-50 p-2 rounded-lg border border-slate-100 font-mono">
              <div>
                <span className="text-slate-400 block">Availability</span>
                <span className="text-slate-800">{r.data_availability_status}</span>
              </div>
              <div>
                <span className="text-slate-400 block">Data Type</span>
                <span className="text-slate-800">{r.data_type}</span>
              </div>
            </div>
          </div>
        ))}
      </div>

      {/* Desktop Main Table (>=768px) */}
      <div className="hidden md:block bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-100 text-slate-700 uppercase font-semibold border-b">
              <tr>
                <th className="py-3 px-4">Record ID</th>
                <th className="py-3 px-4">District / State</th>
                <th className="py-3 px-4">Year / Season</th>
                <th className="py-3 px-4">Risk Score</th>
                <th className="py-3 px-4">Risk Class</th>
                <th className="py-3 px-4">Anomaly Flag</th>
                <th className="py-3 px-4">Data Availability</th>
                <th className="py-3 px-4">Data Type</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {paginated.map((r, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="py-2.5 px-4 font-mono font-semibold text-slate-900">{r.record_id}</td>
                  <td className="py-2.5 px-4">
                    <div className="font-bold text-slate-900">{r.district}</div>
                    <div className="text-[11px] text-slate-400">{r.state}</div>
                  </td>
                  <td className="py-2.5 px-4">{r.year} ({r.season})</td>
                  <td className="py-2.5 px-4 font-bold text-slate-900">{r.risk_score}</td>
                  <td className="py-2.5 px-4">
                    <RiskBadge riskClass={r.risk_class} />
                  </td>
                  <td className="py-2.5 px-4 font-mono">
                    {r.abnormal_pattern_flag === 1 ? (
                      <span className="text-rose-600 font-bold">Abnormal</span>
                    ) : (
                      <span className="text-slate-400">Normal</span>
                    )}
                  </td>
                  <td className="py-2.5 px-4 font-mono text-[11px] text-slate-500">{r.data_availability_status}</td>
                  <td className="py-2.5 px-4 font-mono text-[11px]">
                    <span className={`px-2 py-0.5 rounded ${
                      r.data_type === 'REAL_PUBLIC_SOURCE' ? 'bg-emerald-100 text-emerald-800' : 'bg-blue-100 text-blue-800'
                    }`}>
                      {r.data_type}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {/* Pagination Footer */}
        <div className="p-4 bg-slate-50 border-t flex items-center justify-between text-xs text-slate-600">
          <div>
            Page <strong>{currentPage}</strong> of <strong>{totalPages}</strong> ({filtered.length} items)
          </div>
          <div className="flex items-center space-x-2">
            <button
              disabled={currentPage === 1}
              onClick={() => setCurrentPage(prev => Math.max(prev - 1, 1))}
              className="p-1.5 rounded border border-slate-300 bg-white hover:bg-slate-100 disabled:opacity-40 min-h-[36px] min-w-[36px]"
            >
              <ChevronLeft className="w-4 h-4" />
            </button>
            <button
              disabled={currentPage === totalPages}
              onClick={() => setCurrentPage(prev => Math.min(prev + 1, totalPages))}
              className="p-1.5 rounded border border-slate-300 bg-white hover:bg-slate-100 disabled:opacity-40 min-h-[36px] min-w-[36px]"
            >
              <ChevronRight className="w-4 h-4" />
            </button>
          </div>
        </div>
      </div>

    </div>
  );
}
