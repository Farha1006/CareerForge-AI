import React from 'react';
import { Link } from 'react-router-dom';
import { Cpu, CheckCircle2, AlertCircle } from 'lucide-react';
import { useCareer } from '../context/CareerContext';

export default function Navbar() {
  const { backendHealthy } = useCareer();

  return (
    <nav className="bg-slate-900 border-b border-slate-800 text-white sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-sky-500 to-indigo-600 flex items-center justify-center shadow-lg shadow-sky-500/20">
              <Cpu className="w-6 h-6 text-white" />
            </div>
            <div>
              <span className="font-bold text-lg tracking-tight bg-gradient-to-r from-white via-slate-200 to-sky-400 bg-clip-text text-transparent">
                CareerForge AI
              </span>
              <span className="block text-[10px] uppercase tracking-wider text-sky-400 font-semibold">
                Career Intelligence Platform
              </span>
            </div>
          </Link>

          <div className="flex items-center gap-4">
            <div
              className={`flex items-center gap-2 text-xs font-medium px-3 py-1.5 rounded-full border ${
                backendHealthy
                  ? 'bg-emerald-950/60 border-emerald-800/80 text-emerald-300'
                  : 'bg-rose-950/60 border-rose-800/80 text-rose-300'
              }`}
            >
              {backendHealthy ? (
                <>
                  <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                  <span>FastAPI Backend Online</span>
                </>
              ) : (
                <>
                  <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
                  <span>Backend Offline</span>
                </>
              )}
            </div>

            <Link
              to="/profile"
              className="bg-sky-600 hover:bg-sky-500 text-white text-xs font-semibold px-4 py-2 rounded-lg transition-all shadow-sm shadow-sky-600/30"
            >
              Analyze Profile
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}
