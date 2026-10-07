import React from 'react';
import { Terminal, CheckCircle, AlertCircle, RefreshCw, Clock } from 'lucide-react';
import { ExecutionEvent } from '../types';

interface ExecutionTraceProps {
  events?: ExecutionEvent[];
}

export const ExecutionTrace: React.FC<ExecutionTraceProps> = ({ events = [] }) => {
  const safeEvents = Array.isArray(events) ? events : [];

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <Terminal className="w-5 h-5 text-emerald-400" />
          <h3 className="font-semibold text-sm text-white">Live Execution Trace</h3>
        </div>
        <span className="text-[10px] font-mono px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
          SSE Stream Active
        </span>
      </div>

      <div className="space-y-2.5 max-h-[420px] overflow-y-auto pr-1">
        {safeEvents.length === 0 ? (
          <div className="p-4 text-center text-xs text-slate-400 italic">
            Waiting for agent execution events...
          </div>
        ) : (
          safeEvents.map((ev, idx) => {
            const isSuccess = ev.status === 'completed';
            const isFailed = ev.status === 'failed';
            const isRetry = ev.status === 'retry';

            return (
              <div
                key={idx}
                className={`p-3 rounded-xl border text-xs transition-all ${
                  isFailed
                    ? 'bg-rose-950/20 border-rose-900/40 text-rose-300'
                    : isRetry
                    ? 'bg-amber-950/20 border-amber-900/40 text-amber-300'
                    : 'bg-slate-900/60 border-slate-800 text-slate-300'
                }`}
              >
                <div className="flex items-center justify-between font-mono text-[11px] mb-1">
                  <div className="flex items-center space-x-1.5">
                    {isSuccess ? (
                      <CheckCircle className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                    ) : isFailed ? (
                      <AlertCircle className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                    ) : isRetry ? (
                      <RefreshCw className="w-3.5 h-3.5 text-amber-400 animate-spin shrink-0" />
                    ) : (
                      <Clock className="w-3.5 h-3.5 text-blue-400 shrink-0" />
                    )}
                    <span className="font-semibold text-white">{ev.step}</span>
                  </div>

                  {ev.duration_ms ? (
                    <span className="text-slate-400">{ev.duration_ms}ms</span>
                  ) : null}
                </div>

                <p className="text-[11px] text-slate-400 pl-5">{ev.description}</p>

                {ev.tool && (
                  <div className="mt-1.5 pl-5 flex items-center space-x-2">
                    <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-slate-800 text-slate-300">
                      Tool: {ev.tool}
                    </span>
                    {ev.retry_count ? (
                      <span className="text-[10px] font-mono px-1.5 py-0.5 rounded bg-amber-950 text-amber-400 border border-amber-800">
                        Retry #{ev.retry_count}
                      </span>
                    ) : null}
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
