export interface SubtaskPlan {
  step_number: number;
  title: string;
  description: string;
  tool_required: string;
  target_criteria: string;
  completed: boolean;
}

export interface ExecutionEvent {
  id?: number;
  task_id: string;
  timestamp: string;
  step: string;
  status: 'started' | 'completed' | 'failed' | 'retry';
  tool?: string;
  description: string;
  duration_ms?: number;
  retry_count?: number;
  details?: any;
}

export interface Claim {
  id?: string;
  claim_text?: string;
  claim?: string;
  evidence: string;
  source: string;
  page?: number;
  verification_status: 'SUPPORTED' | 'VERIFIED' | 'PARTIALLY_SUPPORTED' | 'CONTRADICTED' | 'UNSUPPORTED' | 'CONFLICTING' | 'INSUFFICIENT_EVIDENCE' | 'UNABLE_TO_VERIFY';
  status?: string;
  confidence: number;
  reason?: string;
}

export interface Citation {
  id: string;
  index: number;
  title: string;
  authors: string[];
  year: string;
  source: string;
  page?: number;
  url: string;
  type: string;
}

export interface Task {
  id: string;
  user_query: string;
  status: 'pending' | 'planning' | 'executing' | 'verifying' | 'completed' | 'failed';
  created_at: string;
  completed_at?: string;
  research_goal?: string;
  research_plan?: SubtaskPlan[];
  confidence_score?: number;
  final_report?: string;
  citations?: Citation[];
  error_message?: string;
  events?: ExecutionEvent[];
  claims?: Claim[];
}

export interface MemoryItem {
  id: string;
  topic: string;
  query: string;
  findings: string[];
  sources: string[];
  tags: string[];
  created_at: string;
}

export interface EvaluationResult {
  timestamp: string;
  total_test_tasks: number;
  completion_rate_pct: number;
  claim_verification_accuracy_pct: number;
  unsupported_claim_rate_pct: number;
  citation_correctness_pct: number;
  tool_success_rate_pct: number;
  avg_execution_time_seconds: number;
  task_results: any[];
}
