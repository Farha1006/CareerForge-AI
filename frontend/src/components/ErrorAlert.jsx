import React from 'react';
import { AlertCircle, RefreshCw } from 'lucide-react';

export default function ErrorAlert({ message, onRetry }) {
  return (
    <div className="bg-rose-50 border border-rose-200 rounded-xl p-6 text-rose-800 my-6 shadow-sm">
      <div className="flex items-start gap-4">
        <AlertCircle className="w-6 h-6 text-rose-600 shrink-0 mt-0.5" />
        <div className="flex-1">
          <h4 className="text-sm font-bold text-rose-900">API Communication Error</h4>
          <p className="text-xs text-rose-700 mt-1">{message}</p>
          {onRetry && (
            <button
              onClick={onRetry}
              className="mt-4 flex items-center gap-2 text-xs font-semibold bg-rose-600 text-white px-3 py-1.5 rounded-lg hover:bg-rose-700 transition-colors shadow-sm"
            >
              <RefreshCw className="w-3.5 h-3.5" />
              <span>Retry API Request</span>
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
