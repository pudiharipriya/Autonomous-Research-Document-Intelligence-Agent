import json
import uuid
from datetime import datetime
from typing import List, Dict, Any, Optional
from app.db.database import get_db_connection

class MemoryStore:
    def add_memory(self, topic: str, query: str, findings: List[str], sources: List[str] = None, tags: List[str] = None) -> Dict[str, Any]:
        memory_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        sources = sources or []
        tags = tags or []

        conn = get_db_connection()
        conn.execute(
            """INSERT INTO research_memory (id, topic, query, findings, sources, tags, created_at)
               VALUES (?, ?, ?, ?, ?, ?, ?)""",
            (memory_id, topic, query, json.dumps(findings), json.dumps(sources), json.dumps(tags), now)
        )
        conn.commit()
        conn.close()

        return {
            "id": memory_id,
            "topic": topic,
            "query": query,
            "findings": findings,
            "sources": sources,
            "tags": tags,
            "created_at": now
        }

    def list_memories(self) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM research_memory ORDER BY created_at DESC").fetchall()
        conn.close()
        
        result = []
        for r in rows:
            d = dict(r)
            d["findings"] = json.loads(d["findings"])
            d["sources"] = json.loads(d["sources"])
            d["tags"] = json.loads(d["tags"])
            result.append(d)
        return result

    def search_memory(self, query: str) -> List[Dict[str, Any]]:
        memories = self.list_memories()
        q_terms = set(query.lower().split())
        
        matched = []
        for m in memories:
            text = f"{m['topic']} {m['query']} {' '.join(m['findings'])}".lower()
            if any(term in text for term in q_terms):
                matched.append(m)
        return matched

    def clear_all_memory(self):
        conn = get_db_connection()
        conn.execute("DELETE FROM research_memory")
        conn.commit()
        conn.close()

    def delete_memory_by_id(self, memory_id: str):
        conn = get_db_connection()
        conn.execute("DELETE FROM research_memory WHERE id = ?", (memory_id,))
        conn.commit()
        conn.close()

global_memory_store = MemoryStore()
