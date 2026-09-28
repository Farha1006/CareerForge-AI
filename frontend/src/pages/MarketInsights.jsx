import React, { useState } from 'react';
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
  Cell,
  PieChart,
  Pie,
} from 'recharts';
import { BarChart3, TrendingUp, DollarSign, Award, MapPin, GitCommit } from 'lucide-react';
import { useCareer } from '../context/CareerContext';
import MetricCard from '../components/MetricCard';

export default function MarketInsights() {
  const { marketSkills, marketCareers, marketLocations, marketCooccurrences } = useCareer();
  const [activeTab, setActiveTab] = useState('skills');

  const COLORS = ['#0284c7', '#0369a1', '#0d9488', '#059669', '#16a34a', '#65a30d', '#ca8a04', '#d97706'];

  return (
    <div className="space-y-6">
      {/* Top Banner */}
      <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <span className="text-xs font-bold text-sky-600 uppercase tracking-wider block">
            Phase 3 Data Mining & Analytics
          </span>
          <h2 className="text-2xl font-extrabold text-slate-900 mt-1 flex items-center gap-2">
            <BarChart3 className="w-6 h-6 text-sky-600" />
            <span>Job Market Intelligence</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Empirical intelligence mined from 33,245 job postings across 8 career categories and 87 normalized skills.
          </p>
        </div>

        {/* Tab Switchers */}
        <div className="flex bg-slate-100 p-1 rounded-xl shrink-0 self-start sm:self-auto">
          <button
            onClick={() => setActiveTab('skills')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'skills'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            Skill Demand
          </button>
          <button
            onClick={() => setActiveTab('careers')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'careers'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            Career Demand
          </button>
          <button
            onClick={() => setActiveTab('locations')}
            className={`px-3 py-1.5 rounded-lg text-xs font-bold transition-all ${
              activeTab === 'locations'
                ? 'bg-white text-slate-900 shadow-sm'
                : 'text-slate-500 hover:text-slate-900'
            }`}
          >
            Geographic Hotspots
          </button>
        </div>
      </div>

      {/* Top Cards */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
        <MetricCard
          title="Top Demanded Skill"
          value={marketSkills[0]?.skill_name || 'Communication'}
          subtitle={`${marketSkills[0]?.percentage_of_jobs || 48.8}% of total listings`}
          icon={Award}
          color="sky"
        />
        <MetricCard
          title="Top Hiring Domain"
          value={marketCareers[0]?.career_category || 'Management'}
          subtitle={`${marketCareers[0]?.job_count?.toLocaleString() || '11,326'} listings`}
          icon={TrendingUp}
          color="indigo"
        />
        <MetricCard
          title="Highest Tech Salary"
          value="$133,790"
          subtitle="Data, AI & Analytics avg annual salary"
          icon={DollarSign}
          color="emerald"
        />
        <MetricCard
          title="Top Hiring Region"
          value={marketLocations[1]?.location || 'New York, NY'}
          subtitle={`${marketLocations[1]?.job_count || 818} listings (${marketLocations[1]?.percentage_of_jobs || 2.46}%)`}
          icon={MapPin}
          color="amber"
        />
      </div>

      {/* Main Charts Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Top Demanded Skills Chart */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <Award className="w-4 h-4 text-sky-600" />
              <span>Top 10 Demanded Skills (% Market Share)</span>
            </h3>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                layout="vertical"
                data={marketSkills.slice(0, 10)}
                margin={{ top: 5, right: 30, left: 30, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                <XAxis type="number" unit="%" tick={{ fontSize: 11 }} />
                <YAxis dataKey="skill_name" type="category" tick={{ fontSize: 11 }} width={120} />
                <Tooltip formatter={(value) => [`${value}%`, 'Market Share']} />
                <Bar dataKey="percentage_of_jobs" radius={[0, 4, 4, 0]}>
                  {marketSkills.slice(0, 10).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Career Category Volume Chart */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <TrendingUp className="w-4 h-4 text-indigo-600" />
              <span>Job Volume by Career Category</span>
            </h3>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={marketCareers} margin={{ top: 5, right: 20, left: 10, bottom: 65 }}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#f1f5f9" />
                <XAxis
                  dataKey="career_category"
                  tick={{ fontSize: 10 }}
                  interval={0}
                  angle={-35}
                  textAnchor="end"
                />
                <YAxis tick={{ fontSize: 11 }} />
                <Tooltip formatter={(value) => [value.toLocaleString(), 'Postings']} />
                <Bar dataKey="job_count" fill="#6366f1" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Location Hotspots Chart */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <MapPin className="w-4 h-4 text-amber-600" />
              <span>Top Geographic Hiring Regions</span>
            </h3>
          </div>
          <div className="h-72 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart
                layout="vertical"
                data={marketLocations.slice(1, 9)}
                margin={{ top: 5, right: 30, left: 30, bottom: 5 }}
              >
                <CartesianGrid strokeDasharray="3 3" horizontal={false} stroke="#f1f5f9" />
                <XAxis type="number" tick={{ fontSize: 11 }} />
                <YAxis dataKey="location" type="category" tick={{ fontSize: 11 }} width={120} />
                <Tooltip formatter={(value) => [value.toLocaleString(), 'Job Openings']} />
                <Bar dataKey="job_count" fill="#d97706" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Skill Co-occurrence Matrix / Table */}
        <div className="bg-white rounded-2xl p-6 border border-slate-200 shadow-sm space-y-4">
          <div className="flex items-center justify-between border-b border-slate-100 pb-3">
            <h3 className="text-sm font-extrabold text-slate-900 uppercase tracking-wider flex items-center gap-2">
              <GitCommit className="w-4 h-4 text-emerald-600" />
              <span>Top Skill Co-occurrence Pairs</span>
            </h3>
            <span className="text-xs text-slate-400">Data Mined Co-occurrences</span>
          </div>

          <div className="space-y-2 max-h-72 overflow-y-auto pr-1">
            {marketCooccurrences.map((item, idx) => (
              <div
                key={idx}
                className="p-3 rounded-xl border border-slate-100 bg-slate-50/50 flex items-center justify-between"
              >
                <div className="flex items-center gap-2 text-xs">
                  <span className="font-bold text-slate-900">{item.skill_1}</span>
                  <span className="text-slate-400 font-bold">+</span>
                  <span className="font-bold text-sky-700">{item.skill_2}</span>
                </div>
                <div className="text-right">
                  <span className="text-xs font-extrabold text-emerald-700 bg-emerald-50 px-2.5 py-1 rounded-full border border-emerald-100">
                    {item.cooccurrence_count?.toLocaleString()} jobs
                  </span>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
