import React, { useState } from 'react';
import { Header } from './components/Header';
import { Sidebar } from './components/Sidebar';
import { Dashboard } from './pages/Dashboard';
import { NewResearch } from './pages/NewResearch';
import { TaskDetails } from './pages/TaskDetails';
import { MemoryPage } from './pages/MemoryPage';
import { HistoryPage } from './pages/HistoryPage';
import { EvaluationPage } from './pages/EvaluationPage';
import { SettingsPage } from './pages/SettingsPage';
import { AlertCircle, RefreshCw } from 'lucide-react';

interface ErrorBoundaryProps {
  children: React.ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
  error?: Error;
}

class ErrorBoundary extends React.Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): ErrorBoundaryState {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: React.ErrorInfo) {
    console.error('React Component Error:', error, errorInfo);
  }

  render() {
    if (this.state.hasError) {
      return (
        <div className="p-8 max-w-xl mx-auto my-12 glass-panel rounded-2xl border border-rose-900/50 text-center space-y-4">
          <AlertCircle className="w-10 h-10 text-rose-400 mx-auto" />
          <h3 className="text-base font-bold text-white">Something went wrong during rendering</h3>
          <p className="text-xs text-slate-400 font-mono bg-slate-950 p-3 rounded-lg border border-slate-900 text-rose-300">
            {this.state.error?.message || 'Unknown render error'}
          </p>
          <button
            onClick={() => {
              this.setState({ hasError: false });
              window.location.reload();
            }}
            className="px-4 py-2 bg-blue-600 hover:bg-blue-500 text-white rounded-xl text-xs font-semibold inline-flex items-center space-x-2"
          >
            <RefreshCw className="w-4 h-4" />
            <span>Reload Application</span>
          </button>
        </div>
      );
    }
    return this.props.children;
  }
}

export function App() {
  const [activeTab, setActiveTab] = useState<string>('dashboard');
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);

  const handleStartNew = () => {
    setActiveTab('new_research');
    setSelectedTaskId(null);
  };

  const handleViewTask = (taskId: string) => {
    setSelectedTaskId(taskId);
    setActiveTab('task_details');
  };

  const handleTaskCreated = (taskId: string) => {
    setSelectedTaskId(taskId);
    setActiveTab('task_details');
  };

  return (
    <ErrorBoundary>
      <div className="min-h-screen bg-slate-950 text-slate-100 flex flex-col">
        <Header />

        <div className="flex flex-1">
          <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />

          <main className="flex-1 p-8 overflow-y-auto max-h-[calc(100vh-4rem)]">
            {activeTab === 'dashboard' && (
              <Dashboard onStartNew={handleStartNew} onViewTask={handleViewTask} />
            )}

            {activeTab === 'new_research' && (
              <NewResearch onTaskCreated={handleTaskCreated} />
            )}

            {activeTab === 'task_details' && selectedTaskId && (
              <TaskDetails taskId={selectedTaskId} />
            )}

            {activeTab === 'memory' && <MemoryPage />}

            {activeTab === 'history' && <HistoryPage onViewTask={handleViewTask} />}

            {activeTab === 'evaluation' && <EvaluationPage />}

            {activeTab === 'settings' && <SettingsPage />}
          </main>
        </div>
      </div>
    </ErrorBoundary>
  );
}

export default App;
