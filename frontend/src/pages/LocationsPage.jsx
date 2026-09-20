import React, { useEffect, useState } from 'react';
import { MapPin, Search, ArrowUpRight } from 'lucide-react';
import RiskBadge from '../components/RiskBadge';
import { fetchLocations } from '../services/api';

export default function LocationsPage({ dataType, onSelectLocation }) {
  const [locations, setLocations] = useState([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadLocs() {
      setLoading(true);
      try {
        const res = await fetchLocations(dataType);
        setLocations(res.locations || []);
      } catch (err) {
        console.error("Error fetching locations:", err);
      } finally {
        setLoading(false);
      }
    }
    loadLocs();
  }, [dataType]);

  const filtered = locations.filter(l => 
    !search || 
    (l.district && l.district.toLowerCase().includes(search.toLowerCase())) ||
    (l.state && l.state.toLowerCase().includes(search.toLowerCase()))
  );

  return (
    <div className="space-y-6">
      
      <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-xs flex flex-col md:flex-row md:items-center justify-between gap-4">
        <div>
          <h1 className="text-xl font-bold text-slate-900 flex items-center space-x-2">
            <MapPin className="w-6 h-6 text-blue-600" />
            <span>Monitored Locations & Administrative Units</span>
          </h1>
          <p className="text-xs text-slate-500 mt-1">
            Directory of districts and states covered by AquaSentinel AI monitoring engine
          </p>
        </div>

        <div className="relative">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-2.5" />
          <input
            type="text"
            placeholder="Search location..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="pl-9 pr-4 py-2 border border-slate-300 rounded-lg text-xs focus:outline-none focus:ring-2 focus:ring-blue-500 bg-slate-50"
          />
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {filtered.map((loc, i) => (
          <div key={i} className="bg-white p-4 rounded-xl border border-slate-200 shadow-xs flex flex-col justify-between space-y-3">
            <div className="flex items-start justify-between">
              <div>
                <h3 className="font-bold text-slate-900 text-base">{loc.district}</h3>
                <p className="text-xs text-slate-500">{loc.state}</p>
              </div>
              <RiskBadge riskClass={loc.latest_risk_class} score={loc.latest_risk_score} />
            </div>

            <div className="text-[11px] text-slate-400 font-mono">
              Coordinates: {loc.latitude ? `${loc.latitude.toFixed(2)}, ${loc.longitude.toFixed(2)}` : 'N/A'}
            </div>

            <button
              onClick={() => onSelectLocation(loc.district)}
              className="w-full bg-blue-50 hover:bg-blue-100 text-blue-700 border border-blue-200 text-xs font-semibold py-1.5 rounded-lg flex items-center justify-center space-x-1"
            >
              <span>View District Profile</span>
              <ArrowUpRight className="w-3.5 h-3.5" />
            </button>
          </div>
        ))}
      </div>

    </div>
  );
}
