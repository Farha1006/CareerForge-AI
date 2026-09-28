import React from 'react';
import { Loader2 } from 'lucide-react';

export default function LoadingSpinner({ message = 'Running Career Intelligence Engine...' }) {
  return (
    <div className="flex flex-col items-center justify-center p-12 text-center min-h-[300px]">
      <Loader2 className="w-10 h-10 text-sky-600 animate-spin mb-4" />
      <h3 className="text-base font-semibold text-slate-800">{message}</h3>
      <p className="text-xs text-slate-500 mt-1 max-w-sm">
        Synthesizing skill gap analysis, machine learning baseline predictions, PyTorch neural networks, and market demand stats...
      </p>
    </div>
  );
}
