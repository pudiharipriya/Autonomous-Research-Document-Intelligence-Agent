import React from 'react';
import { CheckCircle2, Circle, Clock, Wrench, Target } from 'lucide-react';
import { SubtaskPlan } from '../types';

interface PlanViewerProps {
  goal?: string;
  plan?: SubtaskPlan[];
  currentStep?: number;
}

export const PlanViewer: React.FC<PlanViewerProps> = ({ goal, plan = [], currentStep = 0 }) => {
  const safePlan = Array.isArray(plan) ? plan : [];

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
      <div className="flex items-center space-x-2 pb-3 border-b border-slate-800">
        <Target className="w-5 h-5 text-blue-400" />
        <h3 className="font-semibold text-sm text-white">Autonomous Research Plan</h3>
      </div>

      {goal && (
        <div className="p-3 rounded-xl bg-blue-950/30 border border-blue-900/40 text-xs text-blue-200">
          <span className="font-semibold text-blue-400">Objective:</span> {goal}
        </div>
      )}

      <div className="space-y-3">
        {safePlan.length === 0 ? (
          <p className="text-xs text-slate-400 italic text-center py-4">Research plan initializing...</p>
        ) : (
          safePlan.map((step, idx) => {
            const isDone = step.completed || idx + 1 < currentStep;
            const isCurrent = idx + 1 === currentStep;

            return (
              <div
                key={step.step_number || idx}
                className={`p-3.5 rounded-xl border transition-all ${
                  isCurrent
                    ? 'bg-slate-900 border-blue-500/50 shadow-md shadow-blue-500/10'
                    : isDone
                    ? 'bg-slate-900/40 border-slate-800/80 opacity-80'
                    : 'bg-slate-950/40 border-slate-900'
                }`}
              >
                <div className="flex items-start justify-between">
                  <div className="flex items-center space-x-2.5">
                    {isDone ? (
                      <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                    ) : isCurrent ? (
                      <Clock className="w-4 h-4 text-blue-400 animate-spin shrink-0" />
                    ) : (
                      <Circle className="w-4 h-4 text-slate-600 shrink-0" />
                    )}
                    <h4 className={`text-xs font-semibold ${isCurrent ? 'text-blue-300' : isDone ? 'text-slate-300' : 'text-slate-400'}`}>
                      Step {step.step_number || idx + 1}: {step.title}
                    </h4>
                  </div>

                  <span className="inline-flex items-center space-x-1 px-2 py-0.5 rounded-md bg-slate-800 text-[10px] text-slate-300 font-mono">
                    <Wrench className="w-3 h-3 text-slate-400" />
                    <span>{step.tool_required}</span>
                  </span>
                </div>

                <p className="text-[11px] text-slate-400 mt-1.5 pl-6 leading-relaxed">{step.description}</p>

                {step.target_criteria && (
                  <p className="text-[10px] text-slate-400 pl-6 mt-1 font-mono italic">
                    Criteria: {step.target_criteria}
                  </p>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
