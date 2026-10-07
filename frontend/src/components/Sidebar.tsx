import React from 'react';
import { LayoutDashboard, PlusCircle, Brain, History, BarChart3, Settings } from 'lucide-react';

interface SidebarProps {
  activeTab: string;
  setActiveTab: (tab: string) => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ activeTab, setActiveTab }) => {
  const navItems = [
    { id: 'dashboard', label: 'Dashboard', icon: LayoutDashboard },
    { id: 'new_research', label: 'New Research Task', icon: PlusCircle },
    { id: 'memory', label: 'Research Memory', icon: Brain },
    { id: 'history', label: 'Task History', icon: History },
    { id: 'evaluation', label: 'Evaluation Metrics', icon: BarChart3 },
    { id: 'settings', label: 'Settings', icon: Settings },
  ];

  return (
    <aside className="w-64 border-r border-slate-800/80 bg-slate-950/60 p-4 flex flex-col justify-between h-[calc(100vh-4rem)]">
      <nav className="space-y-1">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activeTab === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActiveTab(item.id)}
              className={`w-full flex items-center space-x-3 px-3.5 py-2.5 rounded-xl text-sm font-medium transition-all ${
                isActive
                  ? 'bg-blue-600 text-white shadow-lg shadow-blue-600/25'
                  : 'text-slate-400 hover:text-white hover:bg-slate-900/80'
              }`}
            >
              <Icon className={`w-4 h-4 ${isActive ? 'text-white' : 'text-slate-400'}`} />
              <span>{item.label}</span>
            </button>
          );
        })}
      </nav>

      <div className="p-3.5 rounded-xl glass-panel border border-slate-800 text-xs text-slate-400 space-y-1">
        <p className="font-semibold text-slate-200">Autonomous Workflow</p>
        <p className="text-[11px] text-slate-400 leading-relaxed">
          PLAN → SEARCH → RETRIEVE → ANALYZE → VERIFY → REPORT
        </p>
      </div>
    </aside>
  );
};
