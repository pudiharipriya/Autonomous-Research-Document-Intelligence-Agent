import json
import httpx
from typing import List, Dict, Any
from app.config import settings
from app.agents.state import AgentState, SubtaskPlan

class PlannerAgent:
    async def create_plan(self, state: AgentState) -> AgentState:
        """
        Creates a structured, actionable subtask research plan based on user objective and uploaded documents.
        """
        query = state.user_query
        docs = state.uploaded_documents

        # Structured planning rule logic / LLM invocation
        plans = []
        step_id = 1

        if docs:
            plans.append(SubtaskPlan(
                step_number=step_id,
                title="Inspect & Process Uploaded Document",
                description=f"Extract text, page metadata and index chunks for document: {docs[0].get('filename', 'uploaded.pdf')}",
                tool_required="document_tool",
                target_criteria="Document parsed, text extracted into page-preserved semantic chunks."
            ))
            step_id += 1

            plans.append(SubtaskPlan(
                step_number=step_id,
                title="Retrieve Relevant Internal Document Sections",
                description=f"Perform semantic vector retrieval over ingested chunks for query: '{query}'",
                tool_required="retrieval_tool",
                target_criteria="Top-k relevant text chunks retrieved with page numbers."
            ))
            step_id += 1

        plans.append(SubtaskPlan(
            step_number=step_id,
            title="Search Related Academic Research Papers",
            description=f"Query arXiv and Crossref literature databases for external research related to '{query}'",
            tool_required="paper_search_tool",
            target_criteria="Retrieve top academic papers, abstracts, authors and published metadata."
        ))
        step_id += 1

        plans.append(SubtaskPlan(
            step_number=step_id,
            title="Extract & Verify Factual Claims",
            description="Identify core quantitative and methodology claims and evaluate against evidence.",
            tool_required="verifier",
            target_criteria="Extract claims, calculate confidence scores, and assign verification statuses."
        ))
        step_id += 1

        plans.append(SubtaskPlan(
            step_number=step_id,
            title="Generate Comprehensive Final Research Report",
            description="Synthesize findings, compare approaches, attach citations, and highlight open questions.",
            tool_required="reporter",
            target_criteria="Structured Markdown research report with numbered verified citations."
        ))

        state.research_goal = f"Autonomous Research & Intelligence analysis for: {query}"
        state.research_plan = plans
        state.status = "planning"
        return state
