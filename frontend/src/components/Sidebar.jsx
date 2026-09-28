import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  UserCheck,
  Compass,
  Layers,
  BarChart3,
  Map,
  Home,
} from 'lucide-react';

export default function Sidebar() {
  const navItems = [
    { to: '/', label: 'Home Overview', icon: Home },
    { to: '/dashboard', label: 'Master Dashboard', icon: LayoutDashboard },
    { to: '/profile', label: 'Student Profile', icon: UserCheck },
    { to: '/career-analysis', label: 'Career Analysis', icon: Compass },
    { to: '/skill-gap', label: 'Skill Gap', icon: Layers },
    { to: '/market-insights', label: 'Market Insights', icon: BarChart3 },
    { to: '/roadmap', label: 'Learning Roadmap', icon: Map },
  ];

  return (
    <aside className="w-64 bg-slate-900 border-r border-slate-800 shrink-0 hidden md:block">
      <div className="p-4 space-y-1 sticky top-16">
        <div className="px-3 py-2 text-[11px] font-bold text-slate-400 uppercase tracking-wider">
          Platform Views
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-colors ${
                  isActive
                    ? 'bg-sky-600 text-white shadow-md shadow-sky-600/20'
                    : 'text-slate-300 hover:bg-slate-800 hover:text-white'
                }`
              }
            >
              <Icon className="w-4 h-4" />
              <span>{item.label}</span>
            </NavLink>
          );
        })}
      </div>
    </aside>
  );
}
