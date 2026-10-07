from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field

class SubtaskPlan(BaseModel):
    step_number: int
    title: str
    description: str
    tool_required: str  # document_tool, retrieval_tool, search_tool, paper_search_tool, verifier, reporter
    target_criteria: str
    completed: bool = False

class AgentState(BaseModel):
    task_id: str
    user_query: str
    uploaded_documents: List[Dict[str, Any]] = Field(default_factory=list)
    research_goal: str = ""
    research_plan: List[SubtaskPlan] = Field(default_factory=list)
    current_step: int = 0
    completed_steps: List[str] = Field(default_factory=list)
    tool_calls: List[Dict[str, Any]] = Field(default_factory=list)
    retrieved_documents: List[Dict[str, Any]] = Field(default_factory=list)
    retrieved_chunks: List[Dict[str, Any]] = Field(default_factory=list)
    external_sources: List[Dict[str, Any]] = Field(default_factory=list)
    claims: List[str] = Field(default_factory=list)
    verified_claims: List[Dict[str, Any]] = Field(default_factory=list)
    failed_actions: List[Dict[str, Any]] = Field(default_factory=list)
    retry_count: int = 0
    max_retries: int = 3
    confidence: float = 0.0
    intermediate_findings: List[str] = Field(default_factory=list)
    final_report: str = ""
    citations: List[Dict[str, Any]] = Field(default_factory=list)
    memory_items: List[Dict[str, Any]] = Field(default_factory=list)
    status: str = "pending"  # planning, executing, verifying, completed, failed
