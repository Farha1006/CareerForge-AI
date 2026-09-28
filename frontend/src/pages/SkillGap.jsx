import React from 'react';
import { Layers, CheckCircle, AlertTriangle, Zap, Target } from 'lucide-react';
import { useCareer } from '../context/CareerContext';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';
import SkillBadge from '../components/SkillBadge';

export default function SkillGap() {
  const { analysisData, loading, error } = useCareer();

  if (loading) return <LoadingSpinner message="Calculating Skill Gap Coverage..." />;
  if (error) return <ErrorAlert message={error} />;
  if (!analysisData) return <div className="p-8 text-center text-slate-500">No skill gap data available. Submit profile first.</div>;

  const { skill_gap, learning_roadmap } = analysisData;

  return (
    <div className="space-y-6">
      {/* Skill Match Overview Header */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2 text-xs font-bold text-sky-600 uppercase tracking-wider">
              <Target className="w-4 h-4" />
              <span>Skill Coverage Analysis</span>
            </div>
            <h2 className="text-2xl font-extrabold text-slate-900 mt-1">
              {skill_gap.target_career}
            </h2>
          </div>

          <div className="flex items-center gap-3">
            <span className="text-3xl font-black text-emerald-600">
              {skill_gap.skill_match_pct}%
            </span>
            <span className="text-xs font-bold text-slate-500 uppercase tracking-wider">
              Coverage Score
            </span>
          </div>
        </div>

        {/* Progress Bar */}
        <div className="w-full bg-slate-100 rounded-full h-3 overflow-hidden">
          <div
            className="bg-gradient-to-r from-sky-500 to-emerald-500 h-full rounded-full transition-all duration-500"
            style={{ width: `${skill_gap.skill_match_pct}%` }}
          />
        </div>
      </div>

      {/* Matched vs Missing Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {/* Matched Skills Card */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <CheckCircle className="w-5 h-5 text-emerald-600" />
              <span>Matched Skills</span>
            </h3>
            <span className="text-xs font-bold bg-emerald-100 text-emerald-800 px-2.5 py-0.5 rounded-full">
              {skill_gap.matched_skills.length} Skills
            </span>
          </div>

          <div className="flex flex-wrap gap-2">
            {skill_gap.matched_skills.map((s) => (
              <SkillBadge key={s} name={s} matched={true} />
            ))}
            {skill_gap.matched_skills.length === 0 && (
              <p className="text-xs text-slate-400">No matching skills found for this role category.</p>
            )}
          </div>
        </div>

        {/* Missing Skills Card */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-600" />
              <span>Skill Gaps to Address</span>
            </h3>
            <span className="text-xs font-bold bg-rose-100 text-rose-800 px-2.5 py-0.5 rounded-full">
              {skill_gap.missing_skills.length} Gaps
            </span>
          </div>

          <div className="flex flex-wrap gap-2">
            {skill_gap.missing_skills.map((s) => (
              <SkillBadge key={s} name={s} matched={false} />
            ))}
          </div>
        </div>
      </div>

      {/* Priority Gap Matrix */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
        <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
          <Zap className="w-5 h-5 text-amber-500" />
          <span>Priority Gap Breakdown</span>
        </h3>

        <div className="divide-y divide-slate-100">
          {learning_roadmap && learning_roadmap.map((item) => (
            <div key={item.skill} className="py-3 flex flex-col sm:flex-row sm:items-center justify-between gap-2">
              <div>
                <span className="text-sm font-bold text-slate-900">{item.skill}</span>
                <p className="text-xs text-slate-500 mt-0.5">{item.reason}</p>
              </div>
              <div className="flex items-center gap-3">
                <span
                  className={`text-[10px] font-bold uppercase px-2.5 py-1 rounded-full ${
                    item.priority === 'High'
                      ? 'bg-rose-100 text-rose-800 border border-rose-200'
                      : item.priority === 'Medium'
                      ? 'bg-amber-100 text-amber-800 border border-amber-200'
                      : 'bg-slate-100 text-slate-700 border border-slate-200'
                  }`}
                >
                  {item.priority} Priority
                </span>
                <span className="text-xs font-bold text-slate-600 w-16 text-right">
                  {item.market_demand_pct}% Demand
                </span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
