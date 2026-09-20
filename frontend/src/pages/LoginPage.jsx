import React, { useState } from 'react';
import { Droplets, Lock, Mail, ShieldCheck } from 'lucide-react';

export default function LoginPage({ onLogin }) {
  const [email, setEmail] = useState('officer@health.gov.in');
  const [password, setPassword] = useState('jalrakshak2026');
  const [role, setRole] = useState('HEALTH_OFFICIAL');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(role);
  };

  return (
    <div className="min-h-screen bg-slate-950 flex flex-col items-center justify-center p-4">
      <div className="w-full max-w-md bg-slate-900 border border-slate-800 rounded-2xl p-8 shadow-2xl space-y-6">
        
        {/* Header Logo */}
        <div className="text-center space-y-2">
          <div className="inline-flex p-3 bg-blue-600 rounded-xl text-white shadow-lg mb-2">
            <Droplets className="w-8 h-8" />
          </div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">AquaSentinel AI</h1>
          <p className="text-xs text-slate-400 font-medium">
            Community Water-Borne Disease Early Warning System
          </p>
          <span className="inline-block text-[11px] bg-blue-900/50 text-blue-300 border border-blue-700/50 px-2.5 py-0.5 rounded font-mono mt-1">
            "From Water Risk to Early Action."
          </span>
        </div>

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Email Address</label>
            <div className="relative">
              <Mail className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="email"
                required
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Password</label>
            <div className="relative">
              <Lock className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
              <input
                type="password"
                required
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full bg-slate-800 border border-slate-700 rounded-lg pl-9 pr-4 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-semibold text-slate-300 uppercase mb-1">Select Authorization Role</label>
            <select
              value={role}
              onChange={(e) => setRole(e.target.value)}
              className="w-full bg-slate-800 border border-slate-700 rounded-lg px-3 py-2 text-xs text-white focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="HEALTH_OFFICIAL">Authorized Health Official</option>
              <option value="ADMIN">System Administrator</option>
              <option value="FIELD_WORKER">Field Verification Worker</option>
              <option value="VIEWER">Public Viewer</option>
            </select>
          </div>

          <button
            type="submit"
            className="w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-2.5 rounded-lg text-xs shadow-md transition-colors flex items-center justify-center space-x-2"
          >
            <ShieldCheck className="w-4 h-4" />
            <span>Sign In to AquaSentinel Portal</span>
          </button>
        </form>

        <div className="text-[11px] text-slate-500 text-center border-t border-slate-800 pt-4 leading-relaxed">
          Decision-support system for public health officials. Risk scores are early-warning signals, NOT medical diagnoses.
        </div>

      </div>
    </div>
  );
}
