import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
  timeout: 10000,
});

export const checkHealth = async () => {
  const response = await apiClient.get('/health');
  return response.data;
};

export const saveStudentProfile = async (profileData) => {
  const response = await apiClient.post('/student/profile', profileData);
  return response.data;
};

export const analyzeSkillGap = async (studentSkills, targetCareer) => {
  const response = await apiClient.post('/skill-gap', {
    student_skills: studentSkills,
    target_career: targetCareer,
  });
  return response.data;
};

export const getRecommendations = async (profileData) => {
  const response = await apiClient.post('/recommend', profileData);
  return response.data;
};

export const predictCareerML = async (studentSkills, topK = 3) => {
  const response = await apiClient.post('/predict/ml', {
    student_skills: studentSkills,
    top_k: topK,
  });
  return response.data;
};

export const predictCareerDL = async (studentSkills, topK = 3) => {
  const response = await apiClient.post('/predict/deep-learning', {
    student_skills: studentSkills,
    top_k: topK,
  });
  return response.data;
};

export const getTopSkills = async (limit = 20) => {
  const response = await apiClient.get(`/market/top-skills?limit=${limit}`);
  return response.data;
};

export const getCareerDemand = async () => {
  const response = await apiClient.get('/market/careers');
  return response.data;
};

export const getLocationDemand = async (limit = 10) => {
  const response = await apiClient.get(`/market/locations?limit=${limit}`);
  return response.data;
};

export const getSkillCooccurrence = async (limit = 10) => {
  const response = await apiClient.get(`/market/skill-cooccurrence?limit=${limit}`);
  return response.data;
};

export default apiClient;
