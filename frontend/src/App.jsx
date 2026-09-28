import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { CareerProvider } from './context/CareerContext';
import Navbar from './components/Navbar';
import Sidebar from './components/Sidebar';

import Home from './pages/Home';
import Profile from './pages/Profile';
import Dashboard from './pages/Dashboard';
import CareerAnalysis from './pages/CareerAnalysis';
import SkillGap from './pages/SkillGap';
import MarketInsights from './pages/MarketInsights';
import LearningRoadmap from './pages/LearningRoadmap';

export default function App() {
  return (
    <CareerProvider>
      <Router>
        <div className="min-h-screen bg-slate-50 flex flex-col font-sans">
          <Navbar />
          <div className="flex flex-1">
            <Sidebar />
            <main className="flex-1 p-4 sm:p-6 lg:p-8 max-w-7xl mx-auto w-full">
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/profile" element={<Profile />} />
                <Route path="/dashboard" element={<Dashboard />} />
                <Route path="/career-analysis" element={<CareerAnalysis />} />
                <Route path="/skill-gap" element={<SkillGap />} />
                <Route path="/market-insights" element={<MarketInsights />} />
                <Route path="/roadmap" element={<LearningRoadmap />} />
              </Routes>
            </main>
          </div>
        </div>
      </Router>
    </CareerProvider>
  );
}
