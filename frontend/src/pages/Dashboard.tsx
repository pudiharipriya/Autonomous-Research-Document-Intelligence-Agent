import React, { useEffect, useState } from 'react';
import { Compass, Brain, ShieldCheck, PlusCircle, ArrowRight, Activity, CheckCircle, Clock } from 'lucide-react';
import { listAllTasks, getMemories } from '../services/api';
import { Task, MemoryItem } from '../types';

interface DashboardProps {
  onStartNew: () => void;
  onViewTask: (taskId: string) => void;
}

export const Dashboard: React.FC<DashboardProps> = ({ onStartNew, onViewTask }) => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    Promise.all([listAllTasks(), getMemories()])
      .then(([tList, mList]) => {
        setTasks(tList);
        setMemories(mList);
      })
      .catch((err) => console.error(err))
      .finally(() => setLoading(false));
  }, []);

  const completedCount = tasks.filter((t) => t.status === 'completed').length;
  const avgConfidence = tasks.length > 0
    ? (tasks.reduce((acc, t) => acc + (t.confidence_score || 0), 0) / tasks.length).toFixed(2)
    : '0.00';

  return (
    <div className="space-y-6">
      {/* Hero Banner */}
      <div className="glass-panel rounded-3xl p-8 border border-slate-800 relative overflow-hidden bg-gradient-to-r from-blue-950/40 via-slate-900 to-slate-950">
        <div className="relative z-10 max-w-2xl space-y-4">
          <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold">
            <Compass className="w-3.5 h-3.5" />
            <span>Autonomous Intelligence Engine</span>
          </div>

          <h2 className="text-3xl font-extrabold text-white tracking-tight leading-tight">
            Autonomous Deep Research & Document Verification
          </h2>

          <p className="text-slate-300 text-sm leading-relaxed">
            ResearchPilot plans, retrieves academic literature, inspects PDF documents, extracts claims, verifies evidence, and synthesizes structured research reports.
          </p>

          <div className="pt-2 flex items-center space-x-4">
            <button
              onClick={onStartNew}
              className="px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-sm shadow-lg shadow-blue-600/30 flex items-center space-x-2 transition-all"
            >
              <PlusCircle className="w-4 h-4" />
              <span>Launch Research Task</span>
            </button>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-5">
        <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-blue-600/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
            <Activity className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400">Completed Tasks</p>
            <h3 className="text-2xl font-bold text-white">{completedCount}</h3>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-600/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400">
            <ShieldCheck className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400">Avg Claim Confidence</p>
            <h3 className="text-2xl font-bold text-white">{avgConfidence}</h3>
          </div>
        </div>

        <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex items-center space-x-4">
          <div className="w-12 h-12 rounded-xl bg-purple-600/10 border border-purple-500/20 flex items-center justify-center text-purple-400">
            <Brain className="w-6 h-6" />
          </div>
          <div>
            <p className="text-xs text-slate-400">Persistent Memories</p>
            <h3 className="text-2xl font-bold text-white">{memories.length}</h3>
          </div>
        </div>
      </div>

      {/* Recent Research Tasks */}
      <div className="glass-panel rounded-2xl border border-slate-800 p-6 space-y-4">
        <div className="flex items-center justify-between">
          <h3 className="font-semibold text-base text-white">Recent Research Tasks</h3>
          <button onClick={onStartNew} className="text-xs text-blue-400 hover:underline flex items-center space-x-1">
            <span>New Task</span>
            <ArrowRight className="w-3.5 h-3.5" />
          </button>
        </div>

        {tasks.length === 0 ? (
          <div className="text-center py-8 text-slate-400 text-xs space-y-2">
            <p>No research tasks run yet.</p>
            <button onClick={onStartNew} className="text-blue-400 underline font-medium">
              Start your first research query →
            </button>
          </div>
        ) : (
          <div className="space-y-3">
            {tasks.slice(0, 5).map((t) => (
              <div
                key={t.id}
                onClick={() => onViewTask(t.id)}
                className="p-4 rounded-xl glass-panel border border-slate-800 hover:border-blue-500/40 cursor-pointer flex items-center justify-between transition-all"
              >
                <div className="space-y-1">
                  <h4 className="text-xs font-semibold text-white">{t.user_query}</h4>
                  <div className="flex items-center space-x-3 text-[11px] text-slate-400">
                    <span>ID: {t.id}</span>
                    <span>•</span>
                    <span>Created: {new Date(t.created_at).toLocaleDateString()}</span>
                  </div>
                </div>

                <div className="flex items-center space-x-3">
                  <span
                    className={`px-2.5 py-1 rounded-full text-[10px] font-mono font-semibold uppercase ${
                      t.status === 'completed'
                        ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-800'
                        : t.status === 'failed'
                        ? 'bg-rose-950/60 text-rose-400 border border-rose-800'
                        : 'bg-blue-950/60 text-blue-400 border border-blue-800 animate-pulse'
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
