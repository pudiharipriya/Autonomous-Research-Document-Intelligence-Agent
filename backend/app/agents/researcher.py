import time
from typing import Dict, Any
from app.agents.state import AgentState
from app.tools.document_tool import process_document_tool
from app.tools.retrieval_tool import semantic_retrieval_tool
from app.tools.search_tool import research_search_tool
from app.tools.paper_search_tool import research_paper_search_tool
from app.db.models import add_execution_event

class ResearcherAgent:
    async def execute_subtask(self, state: AgentState, plan_step: int) -> AgentState:
        if plan_step >= len(state.research_plan):
            return state

        current_plan = state.research_plan[plan_step]
        tool_name = current_plan.tool_required
        start_time = time.time()

        res_data = {}
        status_event = "completed"

        if tool_name == "document_tool":
            if state.uploaded_documents:
                doc = state.uploaded_documents[0]
                doc_path = doc.get("file_path", "")
                doc_id = doc.get("id", "doc_1")
                res_data = process_document_tool(doc_path, doc_id)
                if res_data.get("status") == "success":
                    state.retrieved_documents.append(res_data)
                else:
                    status_event = "failed"
                    state.failed_actions.append({"step": plan_step, "error": res_data.get("error")})

        elif tool_name == "retrieval_tool":
            res_data = semantic_retrieval_tool(state.user_query, top_k=5)
            if res_data.get("status") == "success":
                chunks = res_data.get("results", [])
                state.retrieved_chunks.extend(chunks)
                state.intermediate_findings.append(
                    f"Retrieved {len(chunks)} relevant document chunks for query '{state.user_query}'."
                )

        elif tool_name == "paper_search_tool":
            res_data = await research_paper_search_tool(state.user_query, max_results=4)
            if res_data.get("status") == "success":
                papers = res_data.get("papers", [])
                state.external_sources.extend(papers)
                state.intermediate_findings.append(
                    f"Discovered {len(papers)} related academic papers from arXiv/Crossref."
                )

        elif tool_name == "search_tool":
            res_data = await research_search_tool(state.user_query, max_results=3)
            if res_data.get("status") == "success":
                results = res_data.get("results", [])
                state.external_sources.extend(results)

        duration_ms = int((time.time() - start_time) * 1000)
        current_plan.completed = True
        state.completed_steps.append(current_plan.title)

        state.tool_calls.append({
            "step": plan_step + 1,
            "tool": tool_name,
            "result_summary": f"Executed {tool_name} successfully.",
            "duration_ms": duration_ms
        })

        add_execution_event(
            task_id=state.task_id,
            step=f"Step {plan_step + 1}: {current_plan.title}",
            status=status_event,
            tool=tool_name,
            description=current_plan.description,
            duration_ms=duration_ms,
            details=res_data
        )

        return state
