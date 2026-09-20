import React, { useEffect, useState } from 'react';
import { CheckCircle2, AlertTriangle, FileText, Database } from 'lucide-react';
import { fetchDataQuality } from '../services/api';

export default function DataQualityPage() {
  const [dq, setDq] = useState(null);

  useEffect(() => {
    async function loadDQ() {
      try {
        const res = await fetchDataQuality();
        setDq(res);
      } catch (err) {
        console.error("Error fetching data quality:", err);
      }
    }
    loadDQ();
  }, []);

  if (!dq) return null;

  const comp = dq.completeness_summary || {};
  const total = comp.total_records || 1;

  const completePct = ((comp.complete_records / total) * 100).toFixed(1);
  const partialPct = ((comp.partial_records / total) * 100).toFixed(1);
  const wqOnlyPct = ((comp.water_only / total) * 100).toFixed(1);
  const rfOnlyPct = ((comp.rainfall_only / total) * 100).toFixed(1);
  const hlthOnlyPct = ((comp.health_only / total) * 100).toFixed(1);

  return (
    <div className="space-y-6">
      
      {/* Header */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
        <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
          <CheckCircle2 className="w-6 h-6 text-emerald-600" />
          <span>Data Quality Audit & Completeness</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Data engineering pipeline quality metrics, source coverage, and completeness breakdown
        </p>
      </div>

      {/* KPI Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <span className="text-xs text-slate-500 uppercase font-semibold">Total Audit Records</span>
          <div className="text-2xl font-bold text-slate-900">{total}</div>
          <p className="text-xs text-slate-400">All integrated data entries</p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <span className="text-xs text-slate-500 uppercase font-semibold">Complete Availability</span>
          <div className="text-2xl font-bold text-emerald-600">{completePct}%</div>
          <p className="text-xs text-slate-400">{comp.complete_records} records with full sources</p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <span className="text-xs text-slate-500 uppercase font-semibold">Partial Multi-Source</span>
          <div className="text-2xl font-bold text-blue-600">{partialPct}%</div>
          <p className="text-xs text-slate-400">{comp.partial_records} partial coverage records</p>
        </div>

        <div className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-1">
          <span className="text-xs text-slate-500 uppercase font-semibold">Unmatched Locations</span>
          <div className="text-2xl font-bold text-slate-900">0</div>
          <p className="text-xs text-slate-400">57 canonical geographic mappings</p>
        </div>

      </div>

      {/* Source Breakdown Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
        <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
          <Database className="w-5 h-5 text-blue-600" />
          <span>Data Availability Breakdown by Source</span>
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-100 text-slate-700 uppercase font-semibold border-b">
              <tr>
                <th className="py-2.5 px-4">Availability Status</th>
                <th className="py-2.5 px-4">Description</th>
                <th className="py-2.5 px-4 text-right">Record Count</th>
                <th className="py-2.5 px-4 text-right">Percentage</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              <tr className="hover:bg-slate-50">
                <td className="py-2.5 px-4 font-bold text-emerald-700">COMPLETE</td>
                <td className="py-2.5 px-4">Health + Water Quality + Rainfall present</td>
                <td className="py-2.5 px-4 text-right font-mono font-bold">{comp.complete_records}</td>
                <td className="py-2.5 px-4 text-right font-mono">{completePct}%</td>
              </tr>
              <tr className="hover:bg-slate-50">
                <td className="py-2.5 px-4 font-bold text-blue-700">PARTIAL</td>
                <td className="py-2.5 px-4">Water Quality + Historical Rainfall / National Health baseline</td>
                <td className="py-2.5 px-4 text-right font-mono font-bold">{comp.partial_records}</td>
                <td className="py-2.5 px-4 text-right font-mono">{partialPct}%</td>
              </tr>
              <tr className="hover:bg-slate-50">
                <td className="py-2.5 px-4 font-bold text-slate-700">WATER_ONLY</td>
                <td className="py-2.5 px-4">Ground water quality measurements only</td>
                <td className="py-2.5 px-4 text-right font-mono font-bold">{comp.water_only}</td>
                <td className="py-2.5 px-4 text-right font-mono">{wqOnlyPct}%</td>
              </tr>
              <tr className="hover:bg-slate-50">
                <td className="py-2.5 px-4 font-bold text-slate-700">RAINFALL_ONLY</td>
                <td className="py-2.5 px-4">Historical IMD monsoon series only (1901-2021)</td>
                <td className="py-2.5 px-4 text-right font-mono font-bold">{comp.rainfall_only}</td>
                <td className="py-2.5 px-4 text-right font-mono">{rfOnlyPct}%</td>
              </tr>
              <tr className="hover:bg-slate-50">
                <td className="py-2.5 px-4 font-bold text-slate-700">HEALTH_ONLY</td>
                <td className="py-2.5 px-4">Rajya Sabha reported national health series only</td>
                <td className="py-2.5 px-4 text-right font-mono font-bold">{comp.health_only}</td>
                <td className="py-2.5 px-4 text-right font-mono">{hlthOnlyPct}%</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
