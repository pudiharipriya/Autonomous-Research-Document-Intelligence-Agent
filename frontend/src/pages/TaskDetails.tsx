import React, { useEffect, useState } from 'react';
import { Compass, RefreshCw, AlertCircle } from 'lucide-react';
import { getTaskDetails } from '../services/api';
import { Task, ExecutionEvent } from '../types';
import { PlanViewer } from '../components/PlanViewer';
import { ExecutionTrace } from '../components/ExecutionTrace';
import { ReportViewer } from '../components/ReportViewer';

interface TaskDetailsProps {
  taskId: string;
}

export const TaskDetails: React.FC<TaskDetailsProps> = ({ taskId }) => {
  const [task, setTask] = useState<Task | null>(null);
  const [events, setEvents] = useState<ExecutionEvent[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchTask = async () => {
    try {
      const data = await getTaskDetails(taskId);
      setTask(data);
      if (data.events) {
        setEvents(data.events);
      }
    } catch (err: any) {
      setError(err.message || 'Failed to fetch task details.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTask();

    // Set up SSE Event Stream for live updates
    const sseUrl = `/api/research/${taskId}/events`;
    const eventSource = new EventSource(sseUrl);

    eventSource.onmessage = (e) => {
      try {
        const evData: ExecutionEvent = JSON.parse(e.data);
        setEvents((prev) => {
          // avoid duplicates
          if (prev.some((item) => item.step === evData.step && item.timestamp === evData.timestamp)) {
            return prev;
          }
          return [...prev, evData];
        });

        // Refetch full task data when status changes or finishes
        fetchTask();
      } catch (err) {
        console.error('SSE JSON error', err);
      }
    };

    eventSource.onerror = (err) => {
      console.warn('SSE connection closed or re-connecting.', err);
    };

    return () => {
      eventSource.close();
    };
  }, [taskId]);

  if (loading) {
    return (
      <div className="flex flex-col items-center justify-center min-h-[400px] space-y-3">
        <RefreshCw className="w-8 h-8 text-blue-400 animate-spin" />
        <p className="text-xs text-slate-400">Loading research task trace state...</p>
      </div>
    );
  }

  if (error || !task) {
    return (
      <div className="p-6 rounded-2xl bg-rose-950/30 border border-rose-900/50 text-xs text-rose-300 flex items-center space-x-3">
        <AlertCircle className="w-5 h-5 text-rose-400 shrink-0" />
        <span>{error || 'Task details unavailable.'}</span>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      {/* Header bar */}
      <div className="glass-panel p-5 rounded-2xl border border-slate-800 flex items-center justify-between">
        <div>
          <div className="flex items-center space-x-3">
            <h2 className="text-lg font-bold text-white">{task.user_query}</h2>
            <span
              className={`px-2.5 py-0.5 rounded-full text-[10px] font-mono font-semibold uppercase ${
                task.status === 'completed'
                  ? 'bg-emerald-950/60 text-emerald-400 border border-emerald-800'
                  : task.status === 'failed'
                  ? 'bg-rose-950/60 text-rose-400 border border-rose-800'
                  : 'bg-blue-950/60 text-blue-400 border border-blue-800 animate-pulse'
              }`}
            >
              {task.status}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">Task ID: {task.id} • Created: {new Date(task.created_at).toLocaleString()}</p>
        </div>

        <button
          onClick={fetchTask}
          className="px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs text-slate-300 flex items-center space-x-1.5"
        >
          <RefreshCw className="w-3.5 h-3.5" />
          <span>Refresh</span>
        </button>
      </div>

      {/* Main Grid: Left Plan, Center Report, Right Execution Trace */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Left Column: Plan & Details (4 cols) */}
        <div className="lg:col-span-4 space-y-6">
          <PlanViewer
            goal={task.research_goal}
            plan={task.research_plan}
            currentStep={events.length}
          />

          <ExecutionTrace events={events} />
        </div>

        {/* Center/Right Column: Final Report & Verification (8 cols) */}
        <div className="lg:col-span-8">
          <ReportViewer
            reportMarkdown={task.final_report}
            citations={task.citations}
            claims={task.claims}
            confidenceScore={task.confidence_score}
          />
        </div>
      </div>
    </div>
  );
};
