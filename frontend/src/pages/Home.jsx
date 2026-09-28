import React from 'react';
import { Link } from 'react-router-dom';
import {
  Cpu,
  Sparkles,
  BarChart2,
  BrainCircuit,
  ArrowRight,
  Database,
  Layers,
  CheckCircle,
} from 'lucide-react';
import { useCareer } from '../context/CareerContext';

export default function Home() {
  const { runAnalysis } = useCareer();

  return (
    <div className="space-y-12 py-4">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-900 via-indigo-950 to-slate-900 text-white p-8 sm:p-12 border border-slate-800 shadow-2xl">
        <div className="max-w-3xl space-y-6 relative z-10">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-sky-500/10 border border-sky-400/20 text-sky-300 text-xs font-semibold">
            <Sparkles className="w-3.5 h-3.5 text-sky-400" />
            <span>Multi-Layer Career Intelligence System</span>
          </div>

          <h1 className="text-4xl sm:text-5xl font-extrabold tracking-tight leading-tight">
            CareerForge AI
          </h1>
          <p className="text-lg text-slate-300 font-light leading-relaxed">
            An Intelligent Career Intelligence Platform powered by Data Engineering, Data Mining, Machine Learning, and PyTorch Deep Learning.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-4">
            <Link
              to="/profile"
              className="bg-sky-500 hover:bg-sky-400 text-white font-bold px-6 py-3.5 rounded-xl transition-all shadow-lg shadow-sky-500/25 flex items-center gap-2 text-sm"
            >
              <span>Analyze My Career Profile</span>
              <ArrowRight className="w-4 h-4" />
            </Link>

            <Link
              to="/dashboard"
              className="bg-slate-800 hover:bg-slate-700 text-slate-200 font-semibold px-6 py-3.5 rounded-xl transition-colors border border-slate-700 text-sm"
            >
              Explore Master Dashboard
            </Link>
          </div>
        </div>

        {/* Decorative Grid Pattern */}
        <div className="absolute right-0 top-0 bottom-0 w-1/3 opacity-10 bg-[radial-gradient(#38bdf8_1px,transparent_1px)] [background-size:16px_16px] pointer-events-none" />
      </section>

      {/* Platform Pillars */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-3">
          <div className="w-12 h-12 rounded-xl bg-sky-100 text-sky-600 flex items-center justify-center font-bold">
            <Database className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">Data Engineering</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Cleaned ETL pipeline processing 33,245 job listings stored in SQLite database with normalized schema.
          </p>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-3">
          <div className="w-12 h-12 rounded-xl bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold">
            <BarChart2 className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">Data Mining</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Pairwise skill co-occurrence mining, market demand distribution, and salary benchmark intelligence.
          </p>
        </div>

        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-3">
          <div className="w-12 h-12 rounded-xl bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold">
            <BrainCircuit className="w-6 h-6" />
          </div>
          <h3 className="text-lg font-bold text-slate-900">ML & Deep Learning</h3>
          <p className="text-xs text-slate-600 leading-relaxed">
            Random Forest & PyTorch 3-layer Deep Neural Network predicting career categories with softmax confidence.
          </p>
        </div>
      </section>
    </div>
  );
}
