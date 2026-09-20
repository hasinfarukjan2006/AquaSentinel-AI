import React, { useEffect, useState } from 'react';
import { Activity, ShieldCheck, AlertCircle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend } from 'recharts';
import { fetchHealthData } from '../services/api';

export default function HealthTrendsPage({ dataType }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadHealth() {
      setLoading(true);
      try {
        const res = await fetchHealthData(dataType);
        setRecords(res.records || []);
      } catch (err) {
        console.error("Error fetching health data:", err);
      } finally {
        setLoading(false);
      }
    }
    loadHealth();
  }, [dataType]);

  // Static Rajya Sabha official data table for Real mode reference
  const rajyaSabhaRealData = [
    { disease: 'Acute Diarrheal Diseases', c2019: '17,647,630', c2020: '8,934,341', c2021: '5,907,572' },
    { disease: 'Cholera', c2019: '615', c2020: '70', c2021: '209' },
    { disease: 'Viral Hepatitis- A', c2019: '18,475', c2020: '5,303', c2021: '4,077' },
    { disease: 'Viral Hepatitis- E', c2019: '9,634', c2020: '2,362', c2021: '1,359' },
    { disease: 'Leptospirosis', c2019: '7,335', c2020: '4,950', c2021: '6,086' },
  ];

  return (
    <div className="space-y-6">
      
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
        <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
          <Activity className="w-6 h-6 text-blue-600" />
          <span>Community Health Indicator Trends</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Official Reported Water-Borne Disease Cases (Ministry of Health & Family Welfare / Rajya Sabha Question No. 557)
        </p>
      </div>

      {/* Real Rajya Sabha National Official Table */}
      <div className="bg-slate-900 text-white p-5 rounded-xl border border-slate-800 space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div>
            <h2 className="text-base font-bold text-white flex items-center space-x-2">
              <ShieldCheck className="w-5 h-5 text-emerald-400" />
              <span>Official National Public Health Data (Rajya Sabha AU 557)</span>
            </h2>
            <p className="text-xs text-slate-400 mt-0.5">
              Reported cases of water-borne diseases in India (2019–2021)
            </p>
          </div>
          <span className="text-xs bg-emerald-900 text-emerald-300 border border-emerald-700 px-2.5 py-1 rounded font-mono">
            REAL_PUBLIC_SOURCE
          </span>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-300">
            <thead className="bg-slate-800 text-slate-200 uppercase font-semibold">
              <tr>
                <th className="py-2.5 px-4">Water-Borne Disease Category</th>
                <th className="py-2.5 px-4 text-right">Reported Cases (2019)</th>
                <th className="py-2.5 px-4 text-right">Reported Cases (2020)</th>
                <th className="py-2.5 px-4 text-right">Reported Cases (2021)</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800">
              {rajyaSabhaRealData.map((row, i) => (
                <tr key={i} className="hover:bg-slate-800/60">
                  <td className="py-2.5 px-4 font-bold text-white">{row.disease}</td>
                  <td className="py-2.5 px-4 text-right font-mono text-emerald-300">{row.c2019}</td>
                  <td className="py-2.5 px-4 text-right font-mono text-blue-300">{row.c2020}</td>
                  <td className="py-2.5 px-4 text-right font-mono text-indigo-300">{row.c2021}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

      {/* Terminology Integrity Warning */}
      <div className="bg-blue-50 border border-blue-200 p-4 rounded-xl flex items-start space-x-3 text-blue-900 text-xs">
        <AlertCircle className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Public Health Terminology Integrity Note:</span>
          <p className="mt-0.5 leading-relaxed text-blue-800">
            "Health indicators are displayed strictly using official source terminology. Indicators are NOT labelled as 'disease outbreak' unless the original public source explicitly confirms an outbreak."
          </p>
        </div>
      </div>

      {/* Dynamic Records Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="p-4 border-b bg-slate-50 font-bold text-slate-900 text-sm">
          Active Registry Health Entries ({dataType})
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-100 text-slate-700 uppercase font-semibold border-b">
              <tr>
                <th className="py-3 px-4">Location</th>
                <th className="py-3 px-4">Year</th>
                <th className="py-3 px-4">Health Indicator</th>
                <th className="py-3 px-4 text-right">Reported Case Count</th>
                <th className="py-3 px-4">Data Source</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {records.slice(0, 50).map((r, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="py-2.5 px-4 font-bold text-slate-900">{r.district || r.state}</td>
                  <td className="py-2.5 px-4">{r.year}</td>
                  <td className="py-2.5 px-4">{r.health_indicator}</td>
                  <td className="py-2.5 px-4 text-right font-mono font-bold text-slate-900">
                    {r.health_value !== null ? Number(r.health_value).toLocaleString() : '—'}
                  </td>
                  <td className="py-2.5 px-4 text-[11px] text-slate-400">{r.health_source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
