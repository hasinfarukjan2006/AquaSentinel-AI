import React, { useEffect, useState } from 'react';
import { CloudRain, Activity } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import { fetchRainfall } from '../services/api';

export default function RainfallPage({ dataType }) {
  const [records, setRecords] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadRainfall() {
      setLoading(true);
      try {
        const res = await fetchRainfall(dataType);
        setRecords(res.records || []);
      } catch (err) {
        console.error("Error loading rainfall:", err);
      } finally {
        setLoading(false);
      }
    }
    loadRainfall();
  }, [dataType]);

  const chartData = records.slice(0, 30).map(r => ({
    label: `${r.district || r.state} (${r.year})`,
    mm: r.rainfall_mm,
    anomaly: r.rainfall_anomaly || 0
  }));

  return (
    <div className="space-y-6">
      
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs">
        <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
          <CloudRain className="w-6 h-6 text-blue-600" />
          <span>Monsoon & Rainfall Environmental Trends</span>
        </h1>
        <p className="text-xs text-slate-500 mt-1">
          Historical & Seasonal Monsoon Rainfall (IMD Sub-Divisional & Station Records)
        </p>
      </div>

      {/* Rainfall Bar Chart */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
        <h2 className="text-base font-bold text-slate-900">Monsoon Rainfall Measurements (mm)</h2>
        <div className="h-72">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={chartData} margin={{ top: 10, right: 30, left: 20, bottom: 40 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="label" tick={{ fontSize: 10 }} interval={0} angle={-30} textAnchor="end" />
              <YAxis label={{ value: 'Rainfall (mm)', angle: -90, position: 'insideLeft', fontSize: 11 }} />
              <Tooltip />
              <Bar dataKey="mm" fill="#0284c7" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Table */}
      <div className="bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-100 text-slate-700 uppercase font-semibold border-b">
              <tr>
                <th className="py-3 px-4">Location</th>
                <th className="py-3 px-4">Year</th>
                <th className="py-3 px-4">Season/Month</th>
                <th className="py-3 px-4">Monsoon Rainfall (mm)</th>
                <th className="py-3 px-4">Anomaly Z-Score</th>
                <th className="py-3 px-4">Data Source</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {records.slice(0, 50).map((r, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="py-2.5 px-4 font-bold text-slate-900">{r.district || r.state}</td>
                  <td className="py-2.5 px-4">{r.year}</td>
                  <td className="py-2.5 px-4">{r.month || r.season}</td>
                  <td className="py-2.5 px-4 font-mono font-bold text-blue-700">{r.rainfall_mm} mm</td>
                  <td className="py-2.5 px-4 font-mono">
                    <span className={r.rainfall_anomaly > 1.5 ? 'text-amber-600 font-bold' : 'text-slate-700'}>
                      {r.rainfall_anomaly !== undefined ? r.rainfall_anomaly : '0.0'}
                    </span>
                  </td>
                  <td className="py-2.5 px-4 text-[11px] text-slate-400">{r.rainfall_source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
