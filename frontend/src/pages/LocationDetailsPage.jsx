import React, { useEffect, useState } from 'react';
import { MapPin, ShieldAlert, Activity, Droplets, CloudRain, ArrowLeft, CheckCircle2, AlertTriangle } from 'lucide-react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts';
import RiskBadge from '../components/RiskBadge';
import { fetchLocationRisk } from '../services/api';

export default function LocationDetailsPage({ districtName, dataType, onBack }) {
  const [details, setDetails] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadDetails() {
      setLoading(true);
      try {
        const res = await fetchLocationRisk(districtName, dataType);
        setDetails(res);
      } catch (err) {
        console.error("Error loading location details:", err);
      } finally {
        setLoading(false);
      }
    }
    if (districtName) {
      loadDetails();
    }
  }, [districtName, dataType]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64 text-slate-500">
        <Activity className="w-6 h-6 animate-spin mr-2 text-blue-600" />
        <span>Loading Location Risk Profile for '{districtName}'...</span>
      </div>
    );
  }

  if (!details || !details.found) {
    return (
      <div className="bg-white p-8 rounded-xl border border-slate-200 text-center space-y-4">
        <AlertTriangle className="w-10 h-10 text-amber-500 mx-auto" />
        <h2 className="text-lg font-bold text-slate-800">Location Not Found</h2>
        <p className="text-sm text-slate-500">
          No records found for district '{districtName}' under active data mode '{dataType}'.
        </p>
        <button
          onClick={onBack}
          className="bg-blue-600 hover:bg-blue-700 text-white text-xs font-semibold px-4 py-2 rounded-lg"
        >
          Return to Dashboard
        </button>
      </div>
    );
  }

  const latest = details.latest_record;
  
  const componentData = [
    { name: 'Symptom Health (S)', weight: '25%', value: Math.round(latest.health_component * 100) },
    { name: 'Water Quality (W)', weight: '25%', value: Math.round(latest.water_component * 100) },
    { name: 'Environmental (E)', weight: '20%', value: Math.round(latest.env_component * 100) },
    { name: 'Historical Risk (H)', weight: '15%', value: Math.round(latest.hist_component * 100) },
    { name: 'Vulnerability (V)', weight: '10%', value: Math.round(latest.vuln_component * 100) },
    { name: 'Abnormal Pattern (A)', weight: '5%', value: Math.round(latest.abnormal_component * 100) },
  ];

  return (
    <div className="space-y-6">
      
      {/* Top Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={onBack}
          className="flex items-center space-x-1.5 text-slate-600 hover:text-slate-900 text-xs font-semibold bg-white border border-slate-300 px-3 py-1.5 rounded-lg shadow-xs"
        >
          <ArrowLeft className="w-4 h-4" />
          <span>Back to Monitoring</span>
        </button>
        <span className="text-xs text-slate-500 font-mono">Location ID: LOC-{latest.location_id}</span>
      </div>

      {/* Hero Location Card */}
      <div className="bg-slate-900 text-white p-6 rounded-xl border border-slate-800 flex flex-col md:flex-row justify-between gap-6">
        <div className="space-y-2">
          <div className="flex items-center space-x-2">
            <MapPin className="w-6 h-6 text-blue-400" />
            <h1 className="text-2xl font-bold">{latest.district}</h1>
            <span className="text-slate-400 text-sm">({latest.state})</span>
          </div>
          <p className="text-xs text-slate-400">
            Station: {latest.station_location || 'District Aggregated Grid'} • Season: {latest.season} {latest.year}
          </p>
          <div className="flex items-center space-x-2 pt-2">
            <span className="text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded border border-slate-700 font-mono">
              Availability: {latest.data_availability_status}
            </span>
            <span className="text-xs bg-slate-800 text-slate-300 px-2.5 py-1 rounded border border-slate-700 font-mono">
              Type: {latest.data_type}
            </span>
          </div>
        </div>

        <div className="bg-slate-800 p-5 rounded-xl border border-slate-700 flex flex-col items-center justify-center min-w-[200px] text-center">
          <span className="text-xs text-slate-400 font-semibold uppercase">Risk Score Indicator</span>
          <div className="text-4xl font-extrabold text-white my-1">{latest.risk_score} / 100</div>
          <RiskBadge riskClass={latest.risk_class} />
        </div>
      </div>

      {/* Recommended Verification Actions */}
      <div className="bg-blue-50 border border-blue-200 p-4 rounded-xl flex items-start space-x-3 text-blue-900">
        <CheckCircle2 className="w-5 h-5 text-blue-600 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <h3 className="font-bold text-sm">Recommended Decision-Support Action:</h3>
          <p className="text-xs text-blue-800 leading-relaxed">
            "{details.recommended_action}"
          </p>
        </div>
      </div>

      {/* Score Component Breakdown */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
        <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
          <ShieldAlert className="w-5 h-5 text-blue-600" />
          <span>Prototype Risk Score Component Breakdown</span>
        </h2>

        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={componentData} margin={{ top: 10, right: 30, left: 20, bottom: 25 }}>
              <CartesianGrid strokeDasharray="3 3" vertical={false} />
              <XAxis dataKey="name" tick={{ fontSize: 11 }} interval={0} angle={-15} textAnchor="end" />
              <YAxis domain={[0, 100]} label={{ value: 'Normalized Sub-score (0-100)', angle: -90, position: 'insideLeft', fontSize: 11 }} />
              <Tooltip formatter={(value) => [`${value} / 100`, 'Component Score']} />
              <Bar dataKey="value" fill="#2563eb" radius={[4, 4, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Historical Trend Table */}
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs space-y-4">
        <h2 className="text-base font-bold text-slate-900 flex items-center space-x-2">
          <Activity className="w-5 h-5 text-blue-600" />
          <span>Historical Record Entries for {latest.district}</span>
        </h2>

        <div className="overflow-x-auto">
          <table className="w-full text-left text-xs text-slate-600">
            <thead className="bg-slate-50 text-slate-700 uppercase font-semibold border-b">
              <tr>
                <th className="py-2.5 px-3">Year</th>
                <th className="py-2.5 px-3">Season</th>
                <th className="py-2.5 px-3">Risk Score</th>
                <th className="py-2.5 px-3">Risk Class</th>
                <th className="py-2.5 px-3">Anomaly Flag</th>
                <th className="py-2.5 px-3">Data Status</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100">
              {(details.historical_trend || []).map((row, i) => (
                <tr key={i} className="hover:bg-slate-50">
                  <td className="py-2 px-3 font-bold text-slate-900">{row.year}</td>
                  <td className="py-2 px-3">{row.season}</td>
                  <td className="py-2 px-3 font-semibold">{row.risk_score}</td>
                  <td className="py-2 px-3">
                    <RiskBadge riskClass={row.risk_class} />
                  </td>
                  <td className="py-2 px-3">
                    {row.abnormal_pattern_flag === 1 ? 'Abnormal Pattern' : 'Normal'}
                  </td>
                  <td className="py-2 px-3 font-mono text-[11px] text-slate-500">{row.data_availability_status}</td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </div>

    </div>
  );
}
