from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from app.memory.memory_store import global_memory_store
from app.memory.schemas import MemoryItem, MemoryCreate

router = APIRouter(prefix="/api/memory", tags=["Memory"])

@router.get("", response_model=List[MemoryItem])
async def get_all_memories(search: Optional[str] = Query(None)):
    if search:
        return global_memory_store.search_memory(search)
    return global_memory_store.list_memories()

@router.post("", response_model=MemoryItem)
async def create_memory(item: MemoryCreate):
    created = global_memory_store.add_memory(
        topic=item.topic,
        query=item.query,
        findings=item.findings,
        sources=item.sources,
        tags=item.tags
    )
    return created

@router.delete("")
async def clear_all_memories():
    global_memory_store.clear_all_memory()
    return {"status": "cleared", "message": "All long-term research memory cleared successfully."}

@router.delete("/{memory_id}")
async def delete_single_memory(memory_id: str):
    global_memory_store.delete_memory_by_id(memory_id)
    return {"status": "deleted", "memory_id": memory_id}
