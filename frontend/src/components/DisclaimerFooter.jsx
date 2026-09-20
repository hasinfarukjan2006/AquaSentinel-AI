import React from 'react';
import { AlertCircle } from 'lucide-react';

export default function DisclaimerFooter() {
  return (
    <footer className="bg-slate-900 text-slate-400 border-t border-slate-800 py-4 px-6 text-xs">
      <div className="max-w-7xl mx-auto flex items-start space-x-3">
        <AlertCircle className="w-5 h-5 text-amber-500 shrink-0 mt-0.5" />
        <div className="space-y-1">
          <p className="font-semibold text-slate-300">
            AquaSentinel System Disclaimer:
          </p>
          <p className="text-slate-400 leading-relaxed">
            "AquaSentinel is a prototype decision-support system for community-level early warning. Risk scores are not medical diagnoses and do not confirm disease outbreaks. Results require validation by authorized health professionals and appropriate field or laboratory investigation before action."
          </p>
        </div>
      </div>
    </footer>
  );
}
