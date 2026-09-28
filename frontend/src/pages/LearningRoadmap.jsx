import React from 'react';
import { Map, BookOpen, CheckCircle, Award, Sparkles, ArrowRight } from 'lucide-react';
import { useCareer } from '../context/CareerContext';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';

export default function LearningRoadmap() {
  const { analysisData, loading, error } = useCareer();

  if (loading) return <LoadingSpinner message="Generating Personalized Learning Roadmap..." />;
  if (error) return <ErrorAlert message={error} />;
  if (!analysisData) return <div className="p-8 text-center text-slate-500">No learning roadmap data available. Submit profile first.</div>;

  const { learning_roadmap, skill_gap } = analysisData;

  const stageGroups = {
    'Stage 1: Core Foundation': learning_roadmap.filter((item) => item.stage.includes('Stage 1')),
    'Stage 2: Technical Specialization': learning_roadmap.filter((item) => item.stage.includes('Stage 2')),
    'Stage 3: Advanced Mastery': learning_roadmap.filter((item) => item.stage.includes('Stage 3')),
  };

  const stageColors = {
    'Stage 1: Core Foundation': 'border-sky-500 bg-sky-50 text-sky-800',
    'Stage 2: Technical Specialization': 'border-indigo-500 bg-indigo-50 text-indigo-800',
    'Stage 3: Advanced Mastery': 'border-emerald-500 bg-emerald-50 text-emerald-800',
  };

  return (
    <div className="space-y-6">
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <div className="flex items-center gap-2 text-xs font-bold text-sky-600 uppercase tracking-wider">
            <Map className="w-4 h-4" />
            <span>Target Career Learning Pathway</span>
          </div>
          <h2 className="text-2xl font-extrabold text-slate-900 mt-1">
            {skill_gap.target_career} Roadmap
          </h2>
        </div>
        <div className="text-xs text-slate-500 bg-slate-100 px-3 py-1.5 rounded-lg font-semibold">
          {learning_roadmap.length} Priority Skills To Master
        </div>
      </div>

      {/* 3-Stage Timeline Layout */}
      <div className="space-y-6">
        {Object.entries(stageGroups).map(([stageName, items], stageIdx) => (
          <div key={stageName} className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <div className="flex items-center gap-3">
                <span className="w-7 h-7 rounded-full bg-slate-900 text-white flex items-center justify-center text-xs font-bold">
                  {stageIdx + 1}
                </span>
                <h3 className="text-base font-bold text-slate-900">{stageName}</h3>
              </div>
              <span className="text-xs font-semibold text-slate-500">
                {items.length} Skill{items.length !== 1 ? 's' : ''}
              </span>
            </div>

            {items.length === 0 ? (
              <p className="text-xs text-slate-400 py-2">No skills categorized for this stage.</p>
            ) : (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {items.map((item) => (
                  <div
                    key={item.skill}
                    className="p-4 rounded-xl border border-slate-200 hover:border-sky-300 transition-colors bg-slate-50/50 space-y-2"
                  >
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-bold text-slate-900">{item.skill}</span>
                      <span
                        className={`text-[10px] font-bold uppercase px-2 py-0.5 rounded-full ${
                          item.priority === 'High'
                            ? 'bg-rose-100 text-rose-800'
                            : item.priority === 'Medium'
                            ? 'bg-amber-100 text-amber-800'
                            : 'bg-slate-200 text-slate-700'
                        }`}
                      >
                        {item.priority} Priority
                      </span>
                    </div>

                    <p className="text-xs text-slate-600 leading-relaxed">{item.reason}</p>

                    <div className="pt-2 flex items-center justify-between text-[11px] text-slate-500 border-t border-slate-100">
                      <span>Market Demand: <strong>{item.market_demand_pct}%</strong></span>
                      <span className="text-sky-600 font-semibold flex items-center gap-1">
                        <span>Learn Next</span>
                        <ArrowRight className="w-3 h-3" />
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        ))}
      </div>
    </div>
  );
}
