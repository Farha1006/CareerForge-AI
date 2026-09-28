import React from 'react';

export default function MetricCard({ title, value, subtitle, icon: Icon, trend, color = 'sky' }) {
  const colorMap = {
    sky: 'bg-sky-500/10 text-sky-600 border-sky-200',
    indigo: 'bg-indigo-500/10 text-indigo-600 border-indigo-200',
    emerald: 'bg-emerald-500/10 text-emerald-600 border-emerald-200',
    amber: 'bg-amber-500/10 text-amber-600 border-amber-200',
    rose: 'bg-rose-500/10 text-rose-600 border-rose-200',
  };

  return (
    <div className="bg-white rounded-xl border border-slate-200 p-5 shadow-sm hover:shadow-md transition-shadow">
      <div className="flex items-center justify-between">
        <span className="text-xs font-semibold uppercase tracking-wider text-slate-500">
          {title}
        </span>
        {Icon && (
          <div className={`p-2.5 rounded-lg border ${colorMap[color]}`}>
            <Icon className="w-5 h-5" />
          </div>
        )}
      </div>
      <div className="mt-3">
        <div className="text-2xl font-bold text-slate-900 tracking-tight">
          {value}
        </div>
        {subtitle && (
          <p className="text-xs text-slate-500 mt-1 font-medium">{subtitle}</p>
        )}
      </div>
      {trend && (
        <div className="mt-3 text-xs font-semibold text-emerald-600 flex items-center gap-1">
          <span>{trend}</span>
        </div>
      )}
    </div>
  );
}
