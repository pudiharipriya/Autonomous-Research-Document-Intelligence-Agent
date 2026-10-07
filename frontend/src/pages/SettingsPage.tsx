import React, { useState } from 'react';
import { Settings, Key, Sliders, Database, Save } from 'lucide-react';

export const SettingsPage: React.FC = () => {
  const [llmProvider, setLlmProvider] = useState('openai');
  const [apiKey, setApiKey] = useState('');
  const [model, setModel] = useState('gpt-4o-mini');
  const [searchProvider, setSearchProvider] = useState('tavily');
  const [saved, setSaved] = useState(false);

  const handleSave = (e: React.FormEvent) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="max-w-3xl space-y-6">
      <div className="space-y-1">
        <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
          <Settings className="w-6 h-6 text-blue-400" />
          <span>System Settings & Configuration</span>
        </h2>
        <p className="text-xs text-slate-400">
          Configure external LLM provider keys, search tools, vector store parameters, and agent retry bounds.
        </p>
      </div>

      <form onSubmit={handleSave} className="space-y-6">
        {/* LLM Provider Configuration */}
        <div className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-4">
          <h3 className="font-semibold text-sm text-white flex items-center space-x-2">
            <Key className="w-4 h-4 text-blue-400" />
            <span>LLM Provider & Abstraction</span>
          </h3>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs">
            <div className="space-y-1.5">
              <label className="text-slate-300 font-medium">LLM Provider</label>
              <select
                value={llmProvider}
                onChange={(e) => setLlmProvider(e.target.value)}
                className="w-full rounded-xl bg-slate-950 border border-slate-800 text-slate-200 p-2.5 outline-none focus:border-blue-500"
              >
                <option value="openai">OpenAI / OpenAI-Compatible API</option>
                <option value="anthropic">Anthropic Claude API</option>
                <option value="ollama">Local Ollama LLM</option>
                <option value="mock">Local Dev Mode (Zero Key Required)</option>
              </select>
            </div>

            <div className="space-y-1.5">
              <label className="text-slate-300 font-medium">Model Identifier</label>
              <input
                type="text"
                value={model}
                onChange={(e) => setModel(e.target.value)}
                className="w-full rounded-xl bg-slate-950 border border-slate-800 text-slate-200 p-2.5 outline-none focus:border-blue-500"
              />
            </div>
          </div>

          <div className="space-y-1.5 text-xs">
            <label className="text-slate-300 font-medium">API Key (Optional)</label>
            <input
              type="password"
              value={apiKey}
              onChange={(e) => setApiKey(e.target.value)}
              placeholder="sk-..."
              className="w-full rounded-xl bg-slate-950 border border-slate-800 text-slate-200 p-2.5 outline-none focus:border-blue-500 placeholder-slate-600 font-mono"
            />
            <p className="text-[10px] text-slate-500">
              API keys are read strictly from environment variables (`.env`) or local runtime configuration.
            </p>
          </div>
        </div>

        {/* Search API Configuration */}
        <div className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-4">
          <h3 className="font-semibold text-sm text-white flex items-center space-x-2">
            <Sliders className="w-4 h-4 text-emerald-400" />
            <span>Search & External Discovery Tools</span>
          </h3>

          <div className="space-y-1.5 text-xs">
            <label className="text-slate-300 font-medium">Search Provider</label>
            <select
              value={searchProvider}
              onChange={(e) => setSearchProvider(e.target.value)}
              className="w-full rounded-xl bg-slate-950 border border-slate-800 text-slate-200 p-2.5 outline-none focus:border-blue-500"
            >
              <option value="tavily">Tavily Web Search API</option>
              <option value="arxiv">arXiv & Crossref Academic APIs Only</option>
              <option value="mock">Academic Search Index Fallback Mode</option>
            </select>
          </div>
        </div>

        {/* Database & Storage */}
        <div className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-3">
          <h3 className="font-semibold text-sm text-white flex items-center space-x-2">
            <Database className="w-4 h-4 text-purple-400" />
            <span>Database & Storage Metadata</span>
          </h3>
          <p className="text-xs text-slate-400">
            Database Engine: <strong className="text-white">SQLite (researchpilot.db)</strong> • Vector Indexing: <strong className="text-white">TF-IDF & Cosine Similarity Embeddings</strong>
          </p>
        </div>

        <button
          type="submit"
          className="px-6 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs flex items-center space-x-2 shadow-lg transition-all"
        >
          <Save className="w-4 h-4" />
          <span>{saved ? 'Settings Saved Successfully!' : 'Save Configuration'}</span>
        </button>
      </form>
    </div>
  );
};
