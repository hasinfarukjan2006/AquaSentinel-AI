import React, { useEffect, useState } from 'react';
import { Droplets, Info, Search } from 'lucide-react';
import { fetchWaterQuality } from '../services/api';

export default function WaterQualityPage({ dataType }) {
  const [records, setRecords] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadWQData() {
      setLoading(true);
      try {
        const res = await fetchWaterQuality(dataType);
        setRecords(res.records || []);
      } catch (err) {
        console.error("Error fetching water quality:", err);
      } finally {
        setLoading(false);
      }
    }
    loadWQData();
  }, [dataType]);

  const filtered = records.filter(r => 
    !search || 
    (r.district && r.district.toLowerCase().includes(search.toLowerCase())) ||
    (r.station_location && r.station_location.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="space-y-4 sm:space-y-6 pb-16 lg:pb-0">
      
      {/* Header */}
      <div className="bg-white p-4 sm:p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-3">
        <div>
          <h1 className="text-lg sm:text-xl font-bold text-slate-900 flex items-center space-x-2">
            <Droplets className="w-5 h-5 sm:w-6 sm:h-6 text-blue-600" />
            <span>Water Quality Indicators</span>
          </h1>
          <p className="text-xs text-slate-500 mt-0.5">
            Ground water measurements from Central Ground Water Board (CGWB) & Monitoring Stations
          </p>
        </div>

        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Filter district or station..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9 pr-4 py-2 border border-slate-300 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 bg-slate-50 w-full sm:w-64 min-h-[40px]"
          />
        </div>
      </div>

      {/* Mandatory Disclaimer Box */}
      <div className="bg-amber-50 border border-amber-200 p-3.5 sm:p-4 rounded-xl flex items-start space-x-2.5 text-amber-900 text-xs">
        <Info className="w-4 h-4 text-amber-600 shrink-0 mt-0.5" />
        <div>
          <span className="font-bold">Environmental Indicator Notice:</span>
          <p className="mt-0.5 leading-relaxed text-amber-800 text-[11px] sm:text-xs">
            "Water-quality measurements are environmental indicators and do not by themselves confirm the presence of pathogens."
          </p>
        </div>
      </div>

      {/* Mobile Stacked Cards (<768px) */}
      <div className="block md:hidden space-y-3">
        {filtered.slice(0, 50).map((r, i) => (
          <div key={i} className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs space-y-2.5">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-bold text-slate-900 text-base">{r.district}</h3>
                <p className="text-xs text-slate-500">{r.station_location} ({r.state})</p>
              </div>
              <span className="text-[10px] font-mono bg-slate-100 px-2 py-0.5 rounded text-slate-600">
                {r.year}
              </span>
            </div>

            <div className="grid grid-cols-3 gap-2 text-xs bg-slate-50 p-2.5 rounded-lg border border-slate-100 font-mono">
              <div>
                <span className="text-slate-400 text-[10px] block">pH</span>
                <span className={r.ph < 6.5 || r.ph > 8.5 ? 'text-rose-600 font-bold' : 'text-slate-800'}>
                  {r.ph !== null ? r.ph : '—'}
                </span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] block">TDS (mg/L)</span>
                <span className={r.tds_mg_l > 500 ? 'text-amber-700 font-bold' : 'text-slate-800'}>
                  {r.tds_mg_l !== null ? r.tds_mg_l : '—'}
                </span>
              </div>
              <div>
                <span className="text-slate-400 text-[10px] block">NO3 (mg/L)</span>
                <span className={r.no3_mg_l > 45 ? 'text-rose-600 font-bold' : 'text-slate-800'}>
                  {r.no3_mg_l !== null ? r.no3_mg_l : '—'}
                </span>
              </div>
            </div>

            <div className="text-[11px] text-slate-400 font-mono">
              Source: {r.water_source}
            </div>
          </div>
        ))}
      </div>

      {/* Desktop Table (>=768px) */}
      <div className="hidden md:block bg-white rounded-xl border border-slate-200 shadow-xs overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-100 text-slate-700 uppercase font-semibold border-b">
              <tr>
                <th className="py-3 px-3">Station / District</th>
                <th className="py-3 px-3">State</th>
                <th className="py-3 px-3">pH</th>
                <th className="py-3 px-3">EC (µS/cm)</th>
                <th className="py-3 px-3">TDS (mg/L)</th>
                <th className="py-3 px-3">NO3 (mg/L)</th>
                <th className="py-3 px-3">F (mg/L)</th>
                <th className="py-3 px-3">Fe (mg/L)</th>
                <th className="py-3 px-3">Hardness</th>
                <th className="py-3 px-3">Source</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {filtered.slice(0, 100).map((r, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="py-2.5 px-3">
                    <div className="font-bold text-slate-900">{r.district}</div>
                    <div className="text-[11px] text-slate-400">{r.station_location}</div>
                  </td>
                  <td className="py-2.5 px-3">{r.state}</td>
                  <td className="py-2.5 px-3 font-semibold">
                    <span className={r.ph < 6.5 || r.ph > 8.5 ? 'text-rose-600 font-bold' : 'text-slate-800'}>
                      {r.ph !== null ? r.ph : '—'}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 font-mono">{r.ec_us_cm !== null ? r.ec_us_cm : '—'}</td>
                  <td className="py-2.5 px-3 font-mono">
                    <span className={r.tds_mg_l > 500 ? 'text-amber-700 font-bold' : 'text-slate-800'}>
                      {r.tds_mg_l !== null ? r.tds_mg_l : '—'}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 font-mono">
                    <span className={r.no3_mg_l > 45 ? 'text-rose-600 font-bold' : 'text-slate-800'}>
                      {r.no3_mg_l !== null ? r.no3_mg_l : '—'}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 font-mono">
                    <span className={r.f_mg_l > 1.5 ? 'text-orange-600 font-bold' : 'text-slate-800'}>
                      {r.f_mg_l !== null ? r.f_mg_l : '—'}
                    </span>
                  </td>
                  <td className="py-2.5 px-3 font-mono">{r.fe_mg_l !== null ? r.fe_mg_l : '—'}</td>
                  <td className="py-2.5 px-3 font-mono">{r.total_hardness_mg_l !== null ? r.total_hardness_mg_l : '—'}</td>
                  <td className="py-2.5 px-3 text-[11px] text-slate-400">{r.water_source}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
