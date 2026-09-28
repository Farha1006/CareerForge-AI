import React from 'react';
import { Link } from 'react-router-dom';
import {
  LayoutDashboard,
  Compass,
  Award,
  TrendingUp,
  BrainCircuit,
  Map,
  ArrowRight,
  Layers,
  CheckCircle,
} from 'lucide-react';
import { useCareer } from '../context/CareerContext';
import MetricCard from '../components/MetricCard';
import LoadingSpinner from '../components/LoadingSpinner';
import ErrorAlert from '../components/ErrorAlert';
import SkillBadge from '../components/SkillBadge';

export default function Dashboard() {
  const { profile, analysisData, loading, error, runAnalysis } = useCareer();

  if (loading) return <LoadingSpinner message="Synthesizing Career Intelligence Dashboard..." />;
  if (error) return <ErrorAlert message={error} onRetry={() => runAnalysis()} />;
  if (!analysisData) return <div className="p-8 text-center text-slate-500">No dashboard data available.</div>;

  const { career_recommendations, top_ml_prediction, top_dl_prediction, skill_gap, learning_roadmap } = analysisData;
  const topRec = career_recommendations ? career_recommendations[0] : null;

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-bold text-sky-600 uppercase tracking-wider block">
            Student Intelligence Dashboard
          </span>
          <h2 className="text-2xl font-extrabold text-slate-900 mt-1">
            Welcome, {profile.name}
          </h2>
          <p className="text-xs text-slate-500 mt-0.5">
            {profile.degree} • {profile.skills.length} Possessed Skills
          </p>
        </div>

        <Link
          to="/profile"
          className="bg-slate-900 hover:bg-slate-800 text-white text-xs font-semibold px-4 py-2.5 rounded-xl transition-colors shrink-0"
        >
          Update Profile
        </Link>
      </div>

      {/* Metric Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Top Career Recommendation"
          value={topRec ? topRec.career_category : 'N/A'}
          subtitle={`Composite Score: ${topRec ? topRec.composite_score.toFixed(1) : 0}`}
          icon={Compass}
          color="sky"
        />
        <MetricCard
          title="Target Skill Match"
          value={`${skill_gap.skill_match_pct}%`}
          subtitle={`${skill_gap.matched_skills.length} matched / ${skill_gap.missing_skills.length} missing`}
          icon={Award}
          color="emerald"
        />
        <MetricCard
          title="PyTorch DL Prediction"
          value={top_dl_prediction || 'N/A'}
          subtitle="Phase 6 Softmax Neural Network"
          icon={BrainCircuit}
          color="indigo"
        />
        <MetricCard
          title="Random Forest ML"
          value={top_ml_prediction || 'N/A'}
          subtitle="Phase 5 ML Baseline Model"
          icon={TrendingUp}
          color="amber"
        />
      </div>

      {/* Main Grid Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Left Column: Top Recommendations & Predictions (2 Cols) */}
        <div className="lg:col-span-2 space-y-6">
          {/* Top Recommendations Preview */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Compass className="w-5 h-5 text-sky-600" />
                <span>Ranked Recommendations</span>
              </h3>
              <Link to="/career-analysis" className="text-xs font-semibold text-sky-600 hover:text-sky-800 flex items-center gap-1">
                <span>View All</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="space-y-3">
              {career_recommendations && career_recommendations.slice(0, 3).map((item, idx) => (
                <div key={item.career_category} className="p-4 rounded-xl border border-slate-100 bg-slate-50/50 flex items-center justify-between">
                  <div>
                    <span className="text-xs font-bold text-slate-400">#{idx + 1}</span>
                    <h4 className="text-sm font-bold text-slate-900">{item.career_category}</h4>
                    <p className="text-xs text-slate-500 mt-0.5">
                      Skill Match: <strong>{item.skill_match_pct}%</strong> • PyTorch Conf: <strong>{item.deep_learning_confidence_pct}%</strong>
                    </p>
                  </div>
                  <div className="text-right">
                    <span className="text-lg font-extrabold text-sky-600">{item.composite_score.toFixed(1)}</span>
                    <span className="text-[10px] text-slate-400 block font-bold">SCORE</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Skill Gap Summary Card */}
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Layers className="w-5 h-5 text-indigo-600" />
                <span>Skill Coverage Overview</span>
              </h3>
              <Link to="/skill-gap" className="text-xs font-semibold text-sky-600 hover:text-sky-800 flex items-center gap-1">
                <span>Detailed Skill Gap</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              <div>
                <span className="text-xs font-bold text-emerald-700 uppercase tracking-wider block mb-2">
                  Matched Skills ({skill_gap.matched_skills.length})
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {skill_gap.matched_skills.map((s) => (
                    <SkillBadge key={s} name={s} matched={true} />
                  ))}
                </div>
              </div>
              <div>
                <span className="text-xs font-bold text-rose-700 uppercase tracking-wider block mb-2">
                  Missing Skills ({skill_gap.missing_skills.length})
                </span>
                <div className="flex flex-wrap gap-1.5">
                  {skill_gap.missing_skills.slice(0, 5).map((s) => (
                    <SkillBadge key={s} name={s} matched={false} />
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Column: Learning Roadmap Summary (1 Col) */}
        <div className="space-y-6">
          <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
            <div className="flex items-center justify-between border-b border-slate-100 pb-3">
              <h3 className="text-base font-bold text-slate-900 flex items-center gap-2">
                <Map className="w-5 h-5 text-emerald-600" />
                <span>Priority Roadmap</span>
              </h3>
              <Link to="/roadmap" className="text-xs font-semibold text-sky-600 hover:text-sky-800 flex items-center gap-1">
                <span>Full Roadmap</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </Link>
            </div>

            <div className="space-y-3">
              {learning_roadmap && learning_roadmap.slice(0, 5).map((item) => (
                <div key={item.skill} className="p-3 rounded-xl border border-slate-100 bg-slate-50/50 space-y-1">
                  <div className="flex items-center justify-between text-xs">
                    <span className="font-bold text-slate-900">{item.skill}</span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded-full bg-rose-100 text-rose-800">
                      {item.priority}
                    </span>
                  </div>
                  <p className="text-[11px] text-slate-500">{item.stage}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
