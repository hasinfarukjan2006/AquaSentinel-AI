import React from 'react';

export default function RiskBadge({ riskClass, score }) {
  const getClass = (cls) => {
    switch (cls) {
      case 'LOW':
        return 'bg-emerald-100 text-emerald-800 border-emerald-300';
      case 'MODERATE':
        return 'bg-amber-100 text-amber-800 border-amber-300';
      case 'HIGH':
        return 'bg-orange-100 text-orange-800 border-orange-300';
      case 'VERY HIGH':
        return 'bg-rose-100 text-rose-800 border-rose-300';
      case 'CRITICAL':
        return 'bg-purple-100 text-purple-900 border-purple-400 font-bold';
      default:
        return 'bg-slate-100 text-slate-700 border-slate-300';
    }
  };

  return (
    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${getClass(riskClass)}`}>
      {riskClass} {score !== undefined && score !== null && `(${score})`}
    </span>
  );
}
