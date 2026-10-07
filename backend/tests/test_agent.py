import pytest
from app.agents.state import AgentState
from app.agents.graph import research_graph_engine
from app.db.database import init_db

@pytest.mark.asyncio
async def test_agent_graph_execution():
    init_db()
    state = AgentState(
        task_id="test_task_001",
        user_query="Analyze self-attention multi-head Transformer translation models."
    )
    final_state = await research_graph_engine.run(state)
    assert final_state.status == "completed"
    assert len(final_state.research_plan) >= 3
    assert len(final_state.final_report) > 200
    assert "# Executive Summary" in final_state.final_report
    assert "# Research Question" in final_state.final_report
