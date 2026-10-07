import React, { useEffect, useState } from 'react';
import { Brain, Search, Trash2, Tag, Link2 } from 'lucide-react';
import { getMemories, clearAllMemories, deleteMemory } from '../services/api';
import { MemoryItem } from '../types';

export const MemoryPage: React.FC = () => {
  const [memories, setMemories] = useState<MemoryItem[]>([]);
  const [search, setSearch] = useState('');
  const [loading, setLoading] = useState(true);

  const fetchMemories = async (query?: string) => {
    try {
      const data = await getMemories(query);
      setMemories(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchMemories(search);
  }, [search]);

  const handleClearAll = async () => {
    if (window.confirm('Are you sure you want to clear all long-term research memory entries?')) {
      await clearAllMemories();
      fetchMemories();
    }
  };

  const handleDeleteItem = async (id: string) => {
    await deleteMemory(id);
    fetchMemories();
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div className="space-y-1">
          <h2 className="text-2xl font-bold text-white flex items-center space-x-2">
            <Brain className="w-6 h-6 text-purple-400" />
            <span>Persistent Long-Term Research Memory</span>
          </h2>
          <p className="text-xs text-slate-400">
            Stores key empirical findings, verified research claims, and citation references across past agent runs.
          </p>
        </div>

        {memories.length > 0 && (
          <button
            onClick={handleClearAll}
            className="px-3.5 py-2 rounded-xl bg-rose-950/40 hover:bg-rose-900/60 border border-rose-900/60 text-rose-300 text-xs flex items-center space-x-1.5 transition-all"
          >
            <Trash2 className="w-3.5 h-3.5" />
            <span>Clear Memory Store</span>
          </button>
        )}
      </div>

      {/* Search Input */}
      <div className="glass-panel p-3 rounded-2xl border border-slate-800 flex items-center space-x-3">
        <Search className="w-4 h-4 text-slate-400 shrink-0 ml-2" />
        <input
          type="text"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search stored research topics, queries, or tags..."
          className="w-full bg-transparent text-xs text-white placeholder-slate-500 outline-none"
        />
      </div>

      {/* Memory List Grid */}
      <div className="space-y-4">
        {memories.length === 0 ? (
          <div className="glass-panel rounded-2xl p-8 border border-slate-800 text-center text-slate-400 text-xs space-y-2">
            <Brain className="w-8 h-8 text-purple-400/50 mx-auto" />
            <p>No research memory items stored yet.</p>
          </div>
        ) : (
          memories.map((m) => (
            <div key={m.id} className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-3 relative group">
              <div className="flex items-start justify-between">
                <div>
                  <h3 className="font-semibold text-sm text-white">{m.topic}</h3>
                  <p className="text-xs text-blue-400 font-mono mt-0.5">Query: "{m.query}"</p>
                </div>

                <button
                  onClick={() => handleDeleteItem(m.id)}
                  className="text-slate-500 hover:text-rose-400 p-1 rounded transition-colors"
                  title="Delete memory entry"
                >
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>

              <div className="space-y-1.5 bg-slate-950/60 p-3 rounded-xl border border-slate-900 text-xs">
                <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider block">Key Findings:</span>
                <ul className="list-disc list-inside space-y-1 text-slate-300">
                  {m.findings.map((f, idx) => (
                    <li key={idx} className="leading-relaxed">{f}</li>
                  ))}
                </ul>
              </div>

              <div className="flex items-center justify-between text-[11px] text-slate-400 pt-1">
                <div className="flex items-center space-x-2">
                  <Tag className="w-3.5 h-3.5 text-purple-400" />
                  <div className="flex space-x-1.5">
                    {m.tags.map((t, idx) => (
                      <span key={idx} className="px-2 py-0.5 rounded bg-purple-950/40 text-purple-300 text-[10px] border border-purple-900/40">
                        #{t}
                      </span>
                    ))}
                  </div>
                </div>

                <span className="text-[10px] text-slate-500 font-mono">
                  Saved: {new Date(m.created_at).toLocaleDateString()}
                </span>
              </div>
            </div>
          ))
        )}
      </div>
    </div>
  );
};
