import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.db.database import get_db_connection

def create_task(id: str, user_query: str, status: str = "pending") -> Dict[str, Any]:
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO research_tasks (id, user_query, status, created_at) VALUES (?, ?, ?, ?)",
        (id, user_query, status, now)
    )
    conn.commit()
    conn.close()
    return {"id": id, "user_query": user_query, "status": status, "created_at": now}

def update_task_status(
    task_id: str,
    status: str,
    research_goal: Optional[str] = None,
    research_plan: Optional[List[Dict[str, Any]]] = None,
    final_report: Optional[str] = None,
    citations: Optional[List[Dict[str, Any]]] = None,
    confidence_score: Optional[float] = None,
    error_message: Optional[str] = None
):
    conn = get_db_connection()
    updates = ["status = ?"]
    params = [status]

    if research_goal is not None:
        updates.append("research_goal = ?")
        params.append(research_goal)
    if research_plan is not None:
        updates.append("research_plan = ?")
        params.append(json.dumps(research_plan))
    if final_report is not None:
        updates.append("final_report = ?")
        params.append(final_report)
        updates.append("completed_at = ?")
        params.append(datetime.utcnow().isoformat())
    if citations is not None:
        updates.append("citations = ?")
        params.append(json.dumps(citations))
    if confidence_score is not None:
        updates.append("confidence_score = ?")
        params.append(confidence_score)
    if error_message is not None:
        updates.append("error_message = ?")
        params.append(error_message)

    params.append(task_id)
    query = f"UPDATE research_tasks SET {', '.join(updates)} WHERE id = ?"
    conn.execute(query, params)
    conn.commit()
    conn.close()

def get_task(task_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    row = conn.execute("SELECT * FROM research_tasks WHERE id = ?", (task_id,)).fetchone()
    conn.close()
    if not row:
        return None
    data = dict(row)
    if data.get("research_plan"):
        data["research_plan"] = json.loads(data["research_plan"])
    if data.get("citations"):
        data["citations"] = json.loads(data["citations"])
    return data

def list_tasks() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM research_tasks ORDER BY created_at DESC").fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        if d.get("research_plan"):
            d["research_plan"] = json.loads(d["research_plan"])
        result.append(d)
    return result

def add_execution_event(
    task_id: str,
    step: str,
    status: str,
    description: str,
    tool: Optional[str] = None,
    duration_ms: int = 0,
    retry_count: int = 0,
    details: Optional[Dict[str, Any]] = None
):
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO execution_events 
           (task_id, timestamp, step, status, tool, description, duration_ms, retry_count, details) 
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (task_id, now, step, status, tool, description, duration_ms, retry_count, json.dumps(details or {}))
    )
    conn.commit()
    conn.close()

def get_execution_events(task_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute(
        "SELECT * FROM execution_events WHERE task_id = ? ORDER BY id ASC", (task_id,)
    ).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        if d.get("details"):
            d["details"] = json.loads(d["details"])
        result.append(d)
    return result

def add_document(doc_id: str, task_id: Optional[str], filename: str, file_path: str, file_size: int, page_count: int, metadata: Dict[str, Any]) -> Dict[str, Any]:
    now = datetime.utcnow().isoformat()
    conn = get_db_connection()
    conn.execute(
        """INSERT INTO documents (id, task_id, filename, file_path, file_size, page_count, status, created_at, metadata)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (doc_id, task_id, filename, file_path, file_size, page_count, "processed", now, json.dumps(metadata))
    )
    conn.commit()
    conn.close()
    return {"id": doc_id, "filename": filename, "page_count": page_count}

def save_claims(task_id: str, claims: List[Dict[str, Any]]):
    conn = get_db_connection()
    now = datetime.utcnow().isoformat()
    for c in claims:
        claim_id = c.get("id") or str(uuid.uuid4())
        claim_text = c.get("claim_text") or c.get("claim") or ""
        status = c.get("verification_status") or c.get("status") or "INSUFFICIENT_EVIDENCE"
        conn.execute(
            """INSERT OR REPLACE INTO claims (id, task_id, claim_text, evidence, source, page, status, confidence, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                claim_id,
                task_id,
                claim_text,
                c.get("evidence", ""),
                c.get("source", ""),
                c.get("page"),
                status,
                c.get("confidence", 0.0),
                now
            )
        )
    conn.commit()
    conn.close()

def get_claims_by_task(task_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    rows = conn.execute("SELECT * FROM claims WHERE task_id = ?", (task_id,)).fetchall()
    conn.close()
    result = []
    for r in rows:
        d = dict(r)
        d["claim"] = d.get("claim_text", "")
        d["verification_status"] = d.get("status", "INSUFFICIENT_EVIDENCE")
        result.append(d)
    return result
