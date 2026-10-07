import React, { useState } from 'react';
import { Compass, Sparkles, ArrowRight, Loader2, BookOpen } from 'lucide-react';
import { DocumentUploader } from '../components/DocumentUploader';
import { createResearchTask } from '../services/api';

interface NewResearchProps {
  onTaskCreated: (taskId: string) => void;
}

export const NewResearch: React.FC<NewResearchProps> = ({ onTaskCreated }) => {
  const [query, setQuery] = useState('');
  const [docMetadata, setDocMetadata] = useState<any | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const presets = [
    {
      title: "Transformer Architecture & BLEU Benchmarks",
      query: "Analyze this paper, identify the main methodology, findings and limitations, find related recent research, compare the approaches, verify important claims, and prepare a structured research report."
    },
    {
      title: "Multi-Document Comparison & Limits",
      query: "Compare recurrent neural network translation models with self-attention Transformer architectures. Verify claims and dataset benchmarks."
    },
    {
      title: "Vision & Long-Context Research Discovery",
      query: "Search for recent academic research on long-context sequence modeling and state space models. Compare methodologies and verify claims."
    }
  ];

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) {
      setError('Please enter a valid research question or objective.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const docs = docMetadata ? [docMetadata] : [];
      const res = await createResearchTask(query, docs);
      onTaskCreated(res.task_id);
    } catch (err: any) {
      setError(err.message || 'Failed to start research task.');
      setLoading(false);
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      <div className="space-y-1">
        <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Compass className="w-6 h-6 text-blue-400" />
          <span>Launch Autonomous Research Task</span>
        </h2>
        <p className="text-xs text-slate-400">
          Enter a research question and optional PDF paper. ResearchPilot will create a plan, execute tools, verify claims, and build a report.
        </p>
      </div>

      <form onSubmit={handleSubmit} className="space-y-6">
        {/* Research Query Input */}
        <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-3">
          <label className="block text-xs font-semibold text-slate-200">
            Research Question & Objective <span className="text-rose-400">*</span>
          </label>
          <textarea
            rows={4}
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="e.g., Analyze this paper, identify the main methodology, findings and limitations, find related recent research, compare the approaches, verify important claims, and prepare a structured research report."
            className="w-full rounded-xl bg-slate-950/80 border border-slate-800 focus:border-blue-500 focus:ring-1 focus:ring-blue-500 text-xs text-slate-200 p-4 leading-relaxed placeholder-slate-600 outline-none resize-none"
          />
        </div>

        {/* Quick Presets */}
        <div className="space-y-2">
          <span className="text-xs text-slate-400 flex items-center space-x-1.5 font-medium">
            <BookOpen className="w-3.5 h-3.5 text-blue-400" />
            <span>Sample Portfolio Task Presets:</span>
          </span>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {presets.map((preset, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => setQuery(preset.query)}
                className="p-3 rounded-xl glass-panel border border-slate-800 hover:border-blue-500/40 text-left transition-all space-y-1"
              >
                <h4 className="text-xs font-semibold text-blue-300">{preset.title}</h4>
                <p className="text-[11px] text-slate-400 line-clamp-2">{preset.query}</p>
              </button>
            ))}
          </div>
        </div>

        {/* PDF Uploader */}
        <DocumentUploader onDocumentUploaded={setDocMetadata} />

        {error && (
          <div className="p-4 rounded-xl bg-rose-950/30 border border-rose-900/50 text-xs text-rose-300">
            {error}
          </div>
        )}

        <button
          type="submit"
          disabled={loading}
          className="w-full py-3.5 rounded-xl bg-blue-600 hover:bg-blue-500 disabled:opacity-50 text-white font-semibold text-sm shadow-xl shadow-blue-600/30 flex items-center justify-center space-x-2 transition-all"
        >
          {loading ? (
            <>
              <Loader2 className="w-4 h-4 animate-spin" />
              <span>Initializing Agent & Planning...</span>
            </>
          ) : (
            <>
              <Sparkles className="w-4 h-4" />
              <span>Start Autonomous Research Execution</span>
              <ArrowRight className="w-4 h-4" />
            </>
          )}
        </button>
      </form>
    </div>
  );
};
