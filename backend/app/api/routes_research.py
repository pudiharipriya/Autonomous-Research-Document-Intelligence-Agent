import json
import uuid
import asyncio
from fastapi import APIRouter, HTTPException, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from app.db.models import (
    create_task, get_task, list_tasks, get_execution_events, get_claims_by_task
)
from app.agents.state import AgentState
from app.agents.graph import research_graph_engine

router = APIRouter(prefix="/api/research", tags=["Research Tasks"])

class ResearchRequest(BaseModel):
    user_query: str
    document_ids: Optional[List[str]] = Field(default_factory=list)
    instructions: Optional[str] = None
    document_metadata: Optional[List[Dict[str, Any]]] = Field(default_factory=list)

async def _run_agent_background(task_id: str, request: ResearchRequest):
    state = AgentState(
        task_id=task_id,
        user_query=request.user_query,
        uploaded_documents=request.document_metadata or []
    )
    await research_graph_engine.run(state)

@router.post("")
async def create_research_task(
    request: ResearchRequest,
    background_tasks: BackgroundTasks
):
    if not request.user_query or not request.user_query.strip():
        raise HTTPException(status_code=400, detail="Research query cannot be empty.")

    task_id = f"task_{uuid.uuid4().hex[:8]}"
    create_task(task_id, request.user_query, status="pending")

    # Launch agent task in background
    background_tasks.add_task(_run_agent_background, task_id, request)

    return {
        "status": "created",
        "task_id": task_id,
        "user_query": request.user_query,
        "message": "Research task launched autonomously."
    }

@router.get("")
async def get_all_research_tasks():
    return list_tasks()

@router.get("/{task_id}")
async def get_research_task_details(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    events = get_execution_events(task_id)
    claims = get_claims_by_task(task_id)

    task["events"] = events
    task["claims"] = claims
    return task

@router.get("/{task_id}/events")
async def stream_task_events(task_id: str):
    """
    Server-Sent Events (SSE) streaming real-time agent execution trace updates.
    """
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    async def event_generator():
        last_event_id = 0
        while True:
            events = get_execution_events(task_id)
            if len(events) > last_event_id:
                for ev in events[last_event_id:]:
                    yield f"data: {json.dumps(ev)}\n\n"
                last_event_id = len(events)

            current_task = get_task(task_id)
            if current_task and current_task["status"] in ["completed", "failed"]:
                yield f"data: {json.dumps({'step': 'FINAL', 'status': current_task['status'], 'description': 'Research task finished.'})}\n\n"
                break

            await asyncio.sleep(0.8)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

@router.get("/{task_id}/report")
async def get_task_report(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    return {
        "task_id": task_id,
        "status": task["status"],
        "final_report": task.get("final_report", ""),
        "confidence_score": task.get("confidence_score", 0.0)
    }

@router.get("/{task_id}/sources")
async def get_task_sources(task_id: str):
    task = get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found.")

    return {
        "task_id": task_id,
        "citations": task.get("citations", [])
    }
