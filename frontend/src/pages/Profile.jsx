import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UserCheck, Sparkles, Plus, X, ArrowRight } from 'lucide-react';
import { useCareer, defaultStudentProfile } from '../context/CareerContext';

export default function Profile() {
  const { profile, runAnalysis, loading } = useCareer();
  const navigate = useNavigate();

  const [formData, setFormData] = useState(profile || defaultStudentProfile);
  const [skillInput, setSkillInput] = useState('');
  const [interestInput, setInterestInput] = useState('');
  const [errors, setErrors] = useState({});

  const handleAddSkill = () => {
    if (skillInput.trim() && !formData.skills.includes(skillInput.trim())) {
      setFormData({
        ...formData,
        skills: [...formData.skills, skillInput.trim()],
      });
      setSkillInput('');
    }
  };

  const handleRemoveSkill = (skillToRemove) => {
    setFormData({
      ...formData,
      skills: formData.skills.filter((s) => s !== skillToRemove),
    });
  };

  const handleAddInterest = () => {
    if (interestInput.trim() && !formData.interests.includes(interestInput.trim())) {
      setFormData({
        ...formData,
        interests: [...formData.interests, interestInput.trim()],
      });
      setInterestInput('');
    }
  };

  const handleRemoveInterest = (interestToRemove) => {
    setFormData({
      ...formData,
      interests: formData.interests.filter((i) => i !== interestToRemove),
    });
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.name.trim()) newErrors.name = 'Full name is required.';
    if (formData.skills.length === 0) newErrors.skills = 'At least 1 skill is required for career analysis.';
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!validate()) return;
    await runAnalysis(formData);
    navigate('/career-analysis');
  };

  const loadPresetData = () => {
    setFormData({
      student_id: 'STU-2026-001',
      name: 'Alex Chen',
      education: 'Undergraduate',
      degree: 'B.S. Data Science & Analytics',
      skills: ['Python', 'SQL', 'Excel', 'Problem Solving', 'Communication'],
      interests: ['Data Engineering', 'Artificial Intelligence'],
      experience_years: 1.5,
      preferred_location: 'Remote',
      target_career: 'Data, AI & Analytics',
    });
  };

  const loadPresetCloud = () => {
    setFormData({
      student_id: 'STU-2026-002',
      name: 'Sarah Jenkins',
      education: 'Undergraduate',
      degree: 'B.S. Software Engineering',
      skills: ['Java', 'C++', 'Linux', 'Git', 'Communication'],
      interests: ['Cloud Infrastructure', 'DevOps'],
      experience_years: 0.5,
      preferred_location: 'New York, NY',
      target_career: 'Software & Cloud Engineering',
    });
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 bg-white p-6 rounded-2xl border border-slate-200 shadow-sm">
        <div>
          <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
            <UserCheck className="w-5 h-5 text-sky-600" />
            <span>Student Profile Setup</span>
          </h2>
          <p className="text-xs text-slate-500 mt-1">
            Configure your skill profile to trigger the hybrid recommendation engine.
          </p>
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={loadPresetData}
            className="text-xs font-semibold px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition-colors border border-slate-300"
          >
            Load Data Science Preset
          </button>
          <button
            type="button"
            onClick={loadPresetCloud}
            className="text-xs font-semibold px-3 py-2 bg-slate-100 hover:bg-slate-200 text-slate-700 rounded-lg transition-colors border border-slate-300"
          >
            Load Cloud Preset
          </button>
        </div>
      </div>

      <form onSubmit={handleSubmit} className="bg-white rounded-2xl border border-slate-200 p-6 sm:p-8 shadow-sm space-y-6">
        <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Full Name *
            </label>
            <input
              type="text"
              value={formData.name}
              onChange={(e) => setFormData({ ...formData, name: e.target.value })}
              className="w-full text-sm px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
            {errors.name && <p className="text-xs text-rose-600 mt-1 font-medium">{errors.name}</p>}
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Education Level
            </label>
            <select
              value={formData.education}
              onChange={(e) => setFormData({ ...formData, education: e.target.value })}
              className="w-full text-sm px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 bg-white"
            >
              <option value="Undergraduate">Undergraduate</option>
              <option value="Master's">Master's Degree</option>
              <option value="Ph.D.">Ph.D. / Doctorate</option>
              <option value="Diploma">Diploma / Bootcamp</option>
            </select>
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Major / Degree Program
            </label>
            <input
              type="text"
              value={formData.degree}
              onChange={(e) => setFormData({ ...formData, degree: e.target.value })}
              className="w-full text-sm px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Experience (Years)
            </label>
            <input
              type="number"
              step="0.5"
              value={formData.experience_years}
              onChange={(e) => setFormData({ ...formData, experience_years: parseFloat(e.target.value) || 0 })}
              className="w-full text-sm px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Preferred Work Location
            </label>
            <input
              type="text"
              value={formData.preferred_location}
              onChange={(e) => setFormData({ ...formData, preferred_location: e.target.value })}
              className="w-full text-sm px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
          </div>

          <div>
            <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
              Target Career Role (Optional)
            </label>
            <select
              value={formData.target_career || ''}
              onChange={(e) => setFormData({ ...formData, target_career: e.target.value })}
              className="w-full text-sm px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500 bg-white"
            >
              <option value="">No preference (Auto Rank)</option>
              <option value="Data, AI & Analytics">Data, AI & Analytics</option>
              <option value="Software & Cloud Engineering">Software & Cloud Engineering</option>
              <option value="Management & Operations">Management & Operations</option>
              <option value="Sales & Marketing">Sales & Marketing</option>
              <option value="Finance & Accounting">Finance & Accounting</option>
              <option value="Healthcare & Clinical">Healthcare & Clinical</option>
              <option value="Customer Service & Retail">Customer Service & Retail</option>
            </select>
          </div>
        </div>

        {/* Skills Tag Section */}
        <div>
          <label className="block text-xs font-bold text-slate-700 uppercase tracking-wider mb-2">
            Skills Currently Possessed *
          </label>
          <div className="flex gap-2 mb-3">
            <input
              type="text"
              value={skillInput}
              onChange={(e) => setSkillInput(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && (e.preventDefault(), handleAddSkill())}
              placeholder="e.g. Python, SQL, AWS..."
              className="flex-1 text-sm px-4 py-2.5 rounded-xl border border-slate-300 focus:outline-none focus:ring-2 focus:ring-sky-500"
            />
            <button
              type="button"
              onClick={handleAddSkill}
              className="bg-slate-900 text-white px-4 py-2.5 rounded-xl text-xs font-semibold flex items-center gap-1 hover:bg-slate-800 transition-colors"
            >
              <Plus className="w-4 h-4" /> Add
            </button>
          </div>

          <div className="flex flex-wrap gap-2 p-3 bg-slate-50 rounded-xl border border-slate-200 min-h-[60px]">
            {formData.skills.map((skill) => (
              <span
                key={skill}
                className="inline-flex items-center gap-1.5 text-xs font-semibold bg-sky-100 text-sky-800 px-3 py-1 rounded-full border border-sky-200"
              >
                {skill}
                <button type="button" onClick={() => handleRemoveSkill(skill)}>
                  <X className="w-3.5 h-3.5 text-sky-600 hover:text-sky-900" />
                </button>
              </span>
            ))}
          </div>
          {errors.skills && <p className="text-xs text-rose-600 mt-1 font-medium">{errors.skills}</p>}
        </div>

        {/* Submit CTA */}
        <div className="pt-4 border-t border-slate-200 flex justify-end">
          <button
            type="submit"
            disabled={loading}
            className="bg-sky-600 hover:bg-sky-500 text-white font-bold px-8 py-3.5 rounded-xl transition-all shadow-lg shadow-sky-600/30 flex items-center gap-2 text-sm disabled:opacity-50"
          >
            <span>{loading ? 'Analyzing...' : 'Run Career Intelligence Analysis'}</span>
            <ArrowRight className="w-4 h-4" />
          </button>
        </div>
      </form>
    </div>
  );
}
