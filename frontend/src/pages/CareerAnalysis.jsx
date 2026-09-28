import React from 'react';
import { Compass, Sparkles, BrainCircuit, CheckCircle2, AlertTriangle, Layers } from 'lucide-react';
import { useCareer } from '../context/CareerContext';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';
import SkillBadge from '../components/SkillBadge';

export default function CareerAnalysis() {
  const { analysisData, loading, error, runAnalysis } = useCareer();

  if (loading) return <LoadingSpinner message="Executing Hybrid Recommendation Engine..." />;
  if (error) return <ErrorAlert message={error} onRetry={() => runAnalysis()} />;
  if (!analysisData) return <div className="p-8 text-center text-slate-500">No analysis data available. Submit profile first.</div>;

  const { career_recommendations, top_ml_prediction, top_dl_prediction } = analysisData;

  return (
    <div className="space-y-6">
      {/* Model Predictions Header */}
      <div className="bg-gradient-to-r from-slate-900 to-indigo-950 rounded-2xl p-6 text-white border border-slate-800 shadow-lg">
        <div className="flex items-center gap-2 text-xs font-semibold uppercase tracking-wider text-sky-400 mb-2">
          <BrainCircuit className="w-4 h-4" />
          <span>Machine Learning & Deep Learning Baseline Predictions</span>
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700">
            <span className="text-[11px] uppercase tracking-wider text-slate-400 font-bold block mb-1">
              Phase 5 ML Random Forest Model
            </span>
            <div className="text-lg font-bold text-white flex items-center justify-between">
              <span>{top_ml_prediction || 'N/A'}</span>
              <span className="text-xs bg-sky-500/20 text-sky-300 border border-sky-400/30 px-2.5 py-0.5 rounded-full font-semibold">
                Baseline ML
              </span>
            </div>
          </div>

          <div className="bg-slate-800/80 rounded-xl p-4 border border-slate-700">
            <span className="text-[11px] uppercase tracking-wider text-slate-400 font-bold block mb-1">
              Phase 6 PyTorch Deep Neural Network
            </span>
            <div className="text-lg font-bold text-white flex items-center justify-between">
              <span>{top_dl_prediction || 'N/A'}</span>
              <span className="text-xs bg-indigo-500/20 text-indigo-300 border border-indigo-400/30 px-2.5 py-0.5 rounded-full font-semibold">
                Softmax DNN
              </span>
            </div>
          </div>
        </div>
      </div>

      {/* Recommendations List */}
      <div className="space-y-4">
        <h3 className="text-lg font-bold text-slate-900 flex items-center gap-2">
          <Compass className="w-5 h-5 text-sky-600" />
          <span>Ranked Career Recommendations</span>
        </h3>

        {career_recommendations && career_recommendations.map((item, idx) => (
          <div
            key={item.career_category}
            className={`bg-white rounded-2xl border p-6 shadow-sm transition-shadow ${
              idx === 0 ? 'border-sky-500 ring-2 ring-sky-500/10' : 'border-slate-200'
            }`}
          >
            <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-100 pb-4">
              <div>
                <div className="flex items-center gap-2">
                  <span className="text-xs font-bold text-slate-400 uppercase tracking-wider">
                    Rank #{idx + 1}
                  </span>
                  {item.is_student_target && (
                    <span className="text-[10px] uppercase font-bold bg-amber-100 text-amber-800 px-2 py-0.5 rounded-full">
                      Student Target Choice
                    </span>
                  )}
                </div>
                <h4 className="text-xl font-extrabold text-slate-900 mt-1">
                  {item.career_category}
                </h4>
              </div>

              <div className="flex items-center gap-4">
                <div className="text-right">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">
                    Composite Score
                  </span>
                  <span className="text-2xl font-black text-sky-600">
                    {item.composite_score.toFixed(1)}
                  </span>
                </div>
                <div className="text-right pl-4 border-l border-slate-200">
                  <span className="text-[10px] uppercase font-bold text-slate-400 block">
                    Skill Match
                  </span>
                  <span className="text-lg font-bold text-emerald-600">
                    {item.skill_match_pct}%
                  </span>
                </div>
              </div>
            </div>

            {/* Confidence & Market Row */}
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4 my-4 bg-slate-50 p-3 rounded-xl border border-slate-100 text-xs">
              <div>
                <span className="text-slate-500 block">PyTorch DNN Conf.</span>
                <span className="font-bold text-slate-800">{item.deep_learning_confidence_pct}%</span>
              </div>
              <div>
                <span className="text-slate-500 block">Random Forest Conf.</span>
                <span className="font-bold text-slate-800">{item.ml_baseline_confidence_pct}%</span>
              </div>
              <div>
                <span className="text-slate-500 block">Market Listings</span>
                <span className="font-bold text-slate-800">{item.market_demand.total_job_listings.toLocaleString()}</span>
              </div>
              <div>
                <span className="text-slate-500 block">Avg Salary</span>
                <span className="font-bold text-slate-800">
                  {item.market_demand.avg_annual_salary_usd > 0 ? `$${item.market_demand.avg_annual_salary_usd.toLocaleString()}` : 'N/A'}
                </span>
              </div>
            </div>

            {/* Matched & Missing Skills */}
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2">
              <div>
                <span className="text-xs font-bold text-emerald-700 uppercase tracking-wider block mb-2">
                  Matched Skills ({item.matched_skills.length})
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {item.matched_skills.map((s) => (
                    <SkillBadge key={s} name={s} matched={true} />
                  ))}
                  {item.matched_skills.length === 0 && <span className="text-xs text-slate-400">None matched</span>}
                </div>
              </div>

              <div>
                <span className="text-xs font-bold text-rose-700 uppercase tracking-wider block mb-2">
                  Missing Skills ({item.missing_skills.length})
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {item.missing_skills.map((s) => (
                    <SkillBadge key={s} name={s} matched={false} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
