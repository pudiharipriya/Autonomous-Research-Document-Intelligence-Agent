import React, { useEffect, useState } from 'react';
import { History, ArrowRight, ShieldCheck, CheckCircle2 } from 'lucide-react';
import { listAllTasks } from '../services/api';
import { Task } from '../types';

interface HistoryPageProps {
  onViewTask: (taskId: string) => void;
}

export const HistoryPage: React.FC<HistoryPageProps> = ({ onViewTask }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    listAllTasks()
      .then(setTasks)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  return (
    <div className="space-y-6">
      <div className="space-y-1">
        <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
          <History className="w-6 h-6 text-blue-400" />
          <span>Research Tasks Execution History</span>
        </h2>
        <p className="text-xs text-slate-400">
          Browse and inspect past autonomous research runs, trace logs, and generated reports.
        </p>
      </div>

      <div className="glass-panel rounded-2xl border border-slate-800 p-6 space-y-4">
        {tasks.length === 0 ? (
          <p className="text-xs text-slate-400 italic py-6 text-center">No research task history found.</p>
        ) : (
          <div className="space-y-3">
            {tasks.map((t) => (
              <div
                key={t.id}
                onClick={() => onViewTask(t.id)}
                className="p-4 rounded-xl glass-panel border border-slate-800 hover:border-blue-500/40 cursor-pointer flex items-center justify-between transition-all"
              >
                <div className="space-y-1 max-w-xl">
                  <h4 className="text-xs font-semibold text-white leading-snug">{t.user_query}</h4>
                  <div className="flex items-center space-x-3 text-[11px] text-slate-400 font-mono">
                    <span>Task ID: {t.id}</span>
                    <span>•</span>
                    <span>Confidence: {t.confidence_score ?? '0.00'}</span>
                    <span>•</span>
                    <span>Created: {new Date(t.created_at).toLocaleString()}</span>
                  </div>
                </div>

                <div className="flex items-center space-x-3 shrink-0">
                  <span
                    className={`px-2.5 py-1 rounded-full text-[10px] font-mono font-semibold uppercase ${
                      t.status === 'completed'
                        ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-800'
                        : t.status === 'failed'
                        ? 'bg-rose-950/60 text-rose-400 border border-rose-800'
                        : 'bg-blue-950/60 text-blue-400 border border-blue-800'
                    }`}
                  >
                    {t.status}
                  </span>
                  <ArrowRight className="w-4 h-4 text-slate-400" />
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
