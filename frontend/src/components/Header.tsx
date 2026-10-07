import React, { useEffect, useState } from 'react';
import { Compass, Activity, Database, Sparkles } from 'lucide-react';
import { checkHealth } from '../services/api';

export const Header: React.FC = () => {
  const [health, setHealth] = useState<{ status: string; llm_provider: string } | null>(null);

  useEffect(() => {
    checkHealth()
      .then(setHealth)
      .catch(() => setHealth({ status: 'offline', llm_provider: 'mock' }));
  }, []);

  return (
    <header className="h-16 border-b border-slate-800 glass-panel sticky top-0 z-40 px-6 flex items-center justify-between">
      <div className="flex items-center space-x-3">
        <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-blue-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-blue-500/20">
          <Compass className="w-6 h-6 text-white" />
        </div>
        <div>
          <div className="flex items-center space-x-2">
            <h1 className="font-bold text-lg tracking-tight text-white">RESEARCH<span className="text-blue-400">PILOT</span></h1>
            <span className="text-[10px] uppercase font-semibold tracking-wider px-2 py-0.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20">
              Agentic v1.0
            </span>
          </div>
          <p className="text-xs text-slate-400 hidden sm:block">Autonomous Research & Document Intelligence Agent</p>
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs">
          <Activity className={`w-3.5 h-3.5 ${health?.status === 'healthy' ? 'text-emerald-400 animate-pulse' : 'text-rose-400'}`} />
          <span className="text-slate-300 capitalize">{health?.status === 'healthy' ? 'Backend Ready' : 'Connecting...'}</span>
        </div>

        <div className="flex items-center space-x-2 px-3 py-1.5 rounded-lg bg-slate-900/80 border border-slate-800 text-xs text-slate-300">
          <Sparkles className="w-3.5 h-3.5 text-blue-400" />
          <span className="capitalize">LLM: <strong className="text-white">{health?.llm_provider || 'OpenAI API'}</strong></span>
        </div>
      </div>
    </header>
  );
};
