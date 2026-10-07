from pydantic import BaseModel, Field
from typing import List, Optional

class MemoryItem(BaseModel):
    id: str
    topic: str
    query: str
    findings: List[str]
    sources: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    created_at: str

class MemoryCreate(BaseModel):
    topic: str
    query: str
    findings: List[str]
    sources: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
