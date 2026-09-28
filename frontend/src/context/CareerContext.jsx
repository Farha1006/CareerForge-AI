import React, { createContext, useContext, useState, useEffect } from 'react';
import { getRecommendations, getTopSkills, getCareerDemand, getLocationDemand, getSkillCooccurrence, checkHealth } from '../services/api';

const CareerContext = createContext();

export const defaultStudentProfile = {
  student_id: 'STU-2026-001',
  name: 'Alex Chen',
  education: 'Undergraduate',
  degree: 'B.S. Data Science & Computer Science',
  skills: ['Python', 'SQL', 'Excel', 'Problem Solving', 'Communication'],
  interests: ['Data Engineering', 'Artificial Intelligence', 'Cloud Systems'],
  experience_years: 1.5,
  preferred_location: 'Remote',
  target_career: 'Data, AI & Analytics',
};

export const CareerProvider = ({ children }) => {
  const [profile, setProfile] = useState(defaultStudentProfile);
  const [analysisData, setAnalysisData] = useState(null);
  const [marketSkills, setMarketSkills] = useState([]);
  const [marketCareers, setMarketCareers] = useState([]);
  const [marketLocations, setMarketLocations] = useState([]);
  const [marketCooccurrences, setMarketCooccurrences] = useState([]);
  const [loading, setLoading] = useState(false);
  const [backendHealthy, setBackendHealthy] = useState(true);
  const [error, setError] = useState(null);

  // Check backend health on mount
  useEffect(() => {
    checkHealth()
      .then(() => setBackendHealthy(true))
      .catch(() => setBackendHealthy(false));
  }, []);

  // Run full career recommendation pipeline
  const runAnalysis = async (customProfile = null) => {
    const targetProfile = customProfile || profile;
    setLoading(true);
    setError(null);
    try {
      const data = await getRecommendations(targetProfile);
      setAnalysisData(data);
      if (customProfile) {
        setProfile(customProfile);
      }
    } catch (err) {
      console.error('Error fetching recommendations:', err);
      setError(err.response?.data?.detail || err.message || 'Failed to connect to CareerForge AI Backend API.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch market insights stats
  const fetchMarketData = async () => {
    try {
      const [skillsRes, careersRes, locRes, coRes] = await Promise.all([
        getTopSkills(15),
        getCareerDemand(),
        getLocationDemand(10),
        getSkillCooccurrence(10),
      ]);
      setMarketSkills(skillsRes.top_skills || []);
      setMarketCareers(careersRes.career_categories || []);
      setMarketLocations(locRes.locations || []);
      setMarketCooccurrences(coRes.cooccurrences || []);
    } catch (err) {
      console.error('Error fetching market insights:', err);
    }
  };

  useEffect(() => {
    fetchMarketData();
    runAnalysis(defaultStudentProfile);
  }, []);

  return (
    <CareerContext.Provider
      value={{
        profile,
        setProfile,
        analysisData,
        marketSkills,
        marketCareers,
        marketLocations,
        marketCooccurrences,
        loading,
        error,
        backendHealthy,
        runAnalysis,
        fetchMarketData,
      }}
    >
      {children}
    </CareerContext.Provider>
  );
};

export const useCareer = () => useContext(CareerContext);
