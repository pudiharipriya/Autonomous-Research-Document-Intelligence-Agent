import asyncio
from typing import Dict, Any, List, Optional
from app.agents.state import AgentState
from app.agents.planner import PlannerAgent
from app.agents.researcher import ResearcherAgent
from app.agents.verifier import VerifierAgent
from app.agents.reporter import ReporterAgent
from app.db.models import update_task_status, add_execution_event

class ResearchGraphEngine:
    def __init__(self):
        self.planner = PlannerAgent()
        self.researcher = ResearcherAgent()
        self.verifier = VerifierAgent()
        self.reporter = ReporterAgent()

    async def run(self, state: AgentState) -> AgentState:
        """
        Executes the autonomous agent loop:
        PLAN -> TOOL EXECUTION -> VERIFY -> RETRY / REPLAN IF NEEDED -> REPORT -> END
        """
        try:
            # 1. PLAN
            update_task_status(state.task_id, status="planning")
            add_execution_event(
                task_id=state.task_id,
                step="Planning",
                status="started",
                tool="planner",
                description=f"Creating research plan for objective: '{state.user_query}'"
            )
            state = await self.planner.create_plan(state)
            
            update_task_status(
                state.task_id,
                status="executing",
                research_goal=state.research_goal,
                research_plan=[p.model_dump() for p in state.research_plan]
            )
            add_execution_event(
                task_id=state.task_id,
                step="Planning",
                status="completed",
                tool="planner",
                description=f"Created structured research plan with {len(state.research_plan)} subtasks."
            )

            # 2. EXECUTE TOOL SUBTASKS
            for i in range(len(state.research_plan)):
                plan_item = state.research_plan[i]
                if plan_item.tool_required in ["verifier", "reporter"]:
                    continue

                state.current_step = i + 1
                state = await self.researcher.execute_subtask(state, i)

            # 3. VERIFY CLAIMS
            update_task_status(state.task_id, status="verifying")
            state = await self.verifier.verify_research(state)

            # 4. CONDITIONAL ROUTING: RETRY / RE-PLANNING IF EVIDENCE IS INSUFFICIENT
            if state.confidence < 0.20 and state.retry_count < state.max_retries:
                state.retry_count += 1
                add_execution_event(
                    task_id=state.task_id,
                    step="Re-planning / Retry",
                    status="retry",
                    tool="planner",
                    description=f"Confidence low ({state.confidence}). Initiating retry search attempt {state.retry_count}/{state.max_retries}.",
                    retry_count=state.retry_count
                )
                # Additional external search retry
                state = await self.researcher.execute_subtask(state, len(state.research_plan) - 2)
                state = await self.verifier.verify_research(state)

            # 5. REPORT GENERATION
            state = await self.reporter.generate_report(state)
            state.status = "completed"

            return state

        except Exception as e:
            error_msg = f"Agent Loop Execution Error: {str(e)}"
            state.status = "failed"
            update_task_status(state.task_id, status="failed", error_message=error_msg)
            add_execution_event(
                task_id=state.task_id,
                step="Agent Loop",
                status="failed",
                tool="graph_engine",
                description=error_msg
            )
            return state

research_graph_engine = ResearchGraphEngine()
