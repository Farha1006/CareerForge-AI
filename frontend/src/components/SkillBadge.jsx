import React from 'react';

export default function SkillBadge({ name, matched = true }) {
  return (
    <span
      className={`inline-flex items-center gap-1.5 text-xs font-semibold px-2.5 py-1 rounded-full border ${
        matched
          ? 'bg-emerald-50 text-emerald-700 border-emerald-200'
          : 'bg-rose-50 text-rose-700 border-rose-200'
      }`}
    >
      <span
        className={`w-1.5 h-1.5 rounded-full ${
          matched ? 'bg-emerald-500' : 'bg-rose-500'
        }`}
      />
      {name}
    </span>
  );
}
