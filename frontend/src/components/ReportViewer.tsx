import React, { useState } from 'react';
import { marked } from 'marked';
import { FileText, ShieldCheck, Link2, Copy, Check } from 'lucide-react';
import { Citation, Claim } from '../types';
import { VerificationCard } from './VerificationCard';

interface ReportViewerProps {
  reportMarkdown?: string;
  citations?: Citation[];
  claims?: Claim[];
  confidenceScore?: number;
}

export const ReportViewer: React.FC<ReportViewerProps> = ({
  reportMarkdown = '',
  citations = [],
  claims = [],
  confidenceScore = 0.0,
}) => {
  const [activeTab, setActiveTab] = useState<'report' | 'claims' | 'sources'>('report');
  const [copied, setCopied] = useState(false);

  const safeCitations = Array.isArray(citations) ? citations : [];
  const safeClaims = Array.isArray(claims) ? claims : [];
  const safeMarkdown = typeof reportMarkdown === 'string' ? reportMarkdown : '';

  const handleCopy = () => {
    navigator.clipboard.writeText(safeMarkdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  let renderedHtml = '';
  try {
    const rawParsed = marked.parse(safeMarkdown || '*Report is being generated autonomously by ResearchPilot...*');
    renderedHtml = typeof rawParsed === 'string' ? rawParsed : '';
  } catch (e) {
    renderedHtml = '<p>Error formatting markdown report.</p>';
  }

  return (
    <div className="glass-panel rounded-2xl border border-slate-800 flex flex-col h-full overflow-hidden">
      {/* Tab Navigation */}
      <div className="border-b border-slate-800 px-5 py-3 flex items-center justify-between bg-slate-950/60">
        <div className="flex space-x-1 bg-slate-900 p-1 rounded-xl border border-slate-800">
          <button
            onClick={() => setActiveTab('report')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'report' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            <FileText className="w-3.5 h-3.5" />
            <span>Final Report</span>
          </button>

          <button
            onClick={() => setActiveTab('claims')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'claims' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            <ShieldCheck className="w-3.5 h-3.5" />
            <span>Verification ({safeClaims.length})</span>
          </button>

          <button
            onClick={() => setActiveTab('sources')}
            className={`flex items-center space-x-2 px-3 py-1.5 rounded-lg text-xs font-medium transition-all ${
              activeTab === 'sources' ? 'bg-blue-600 text-white shadow-md' : 'text-slate-400 hover:text-white'
            }`}
          >
            <Link2 className="w-3.5 h-3.5" />
            <span>Citations ({safeCitations.length})</span>
          </button>
        </div>

        {safeMarkdown && (
          <button
            onClick={handleCopy}
            className="flex items-center space-x-1.5 px-3 py-1.5 rounded-lg bg-slate-900 hover:bg-slate-800 border border-slate-800 text-xs text-slate-300 transition-all"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied' : 'Copy Markdown'}</span>
          </button>
        )}
      </div>

      {/* Tab Content */}
      <div className="p-6 overflow-y-auto flex-1 max-h-[650px]">
        {activeTab === 'report' && (
          <div
            className="prose prose-invert prose-blue max-w-none text-sm leading-relaxed space-y-4"
            dangerouslySetInnerHTML={{ __html: renderedHtml }}
          />
        )}

        {activeTab === 'claims' && (
          <VerificationCard claims={safeClaims} confidenceScore={confidenceScore} />
        )}

        {activeTab === 'sources' && (
          <div className="space-y-4">
            <h3 className="font-semibold text-sm text-white flex items-center space-x-2">
              <Link2 className="w-4 h-4 text-blue-400" />
              <span>Verified Citations & External Sources</span>
            </h3>

            {safeCitations.length === 0 ? (
              <p className="text-xs text-slate-400 italic">No external citations logged for this task.</p>
            ) : (
              <div className="space-y-3">
                {safeCitations.map((c) => (
                  <div key={c.id} className="p-4 rounded-xl glass-panel border border-slate-800 flex items-start justify-between">
                    <div className="space-y-1 text-xs">
                      <div className="flex items-center space-x-2">
                        <span className="font-mono font-bold text-blue-400">{c.id}</span>
                        <h4 className="font-semibold text-white">{c.title}</h4>
                      </div>
                      <p className="text-slate-400">
                        {Array.isArray(c.authors) ? c.authors.join(', ') : 'Authors'} ({c.year}) • <span className="text-slate-300">{c.source}</span>
                      </p>
                      {c.page && <p className="text-slate-400 font-mono text-[10px]">Indexed Location: Page {c.page}</p>}
                    </div>

                    <a
                      href={c.url}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="px-3 py-1.5 rounded-lg bg-blue-950/40 hover:bg-blue-900/60 border border-blue-900/60 text-blue-400 text-xs font-mono shrink-0 ml-4"
                    >
                      View Link ↗
                    </a>
                  </div>
                ))}
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
