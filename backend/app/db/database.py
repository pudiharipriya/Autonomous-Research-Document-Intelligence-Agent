import sqlite3
import os
import json
from typing import Dict, Any, List, Optional
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "researchpilot.db")

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Research Tasks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS research_tasks (
        id TEXT PRIMARY KEY,
        user_query TEXT NOT NULL,
        status TEXT NOT NULL, -- pending, planning, executing, verifying, completed, failed
        created_at TEXT NOT NULL,
        completed_at TEXT,
        research_goal TEXT,
        research_plan TEXT, -- JSON
        confidence_score REAL DEFAULT 0.0,
        final_report TEXT,
        citations TEXT, -- JSON
        error_message TEXT
    )
    """)

    # Documents table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS documents (
        id TEXT PRIMARY KEY,
        task_id TEXT,
        filename TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_size INTEGER NOT NULL,
        page_count INTEGER NOT NULL,
        status TEXT NOT NULL, -- uploaded, processed, error
        created_at TEXT NOT NULL,
        metadata TEXT, -- JSON
        FOREIGN KEY (task_id) REFERENCES research_tasks (id)
    )
    """)

    # Document Chunks table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS document_chunks (
        id TEXT PRIMARY KEY,
        document_id TEXT NOT NULL,
        chunk_index INTEGER NOT NULL,
        page_number INTEGER NOT NULL,
        content TEXT NOT NULL,
        metadata TEXT, -- JSON
        FOREIGN KEY (document_id) REFERENCES documents (id)
    )
    """)

    # Execution Events table (Trace)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS execution_events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task_id TEXT NOT NULL,
        timestamp TEXT NOT NULL,
        step TEXT NOT NULL,
        status TEXT NOT NULL,
        tool TEXT,
        description TEXT NOT NULL,
        duration_ms INTEGER DEFAULT 0,
        retry_count INTEGER DEFAULT 0,
        details TEXT, -- JSON
        FOREIGN KEY (task_id) REFERENCES research_tasks (id)
    )
    """)

    # Verified Claims table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS claims (
        id TEXT PRIMARY KEY,
        task_id TEXT NOT NULL,
        claim_text TEXT NOT NULL,
        evidence TEXT,
        source TEXT,
        page INTEGER,
        status TEXT NOT NULL, -- VERIFIED, PARTIALLY_SUPPORTED, UNSUPPORTED, CONFLICTING, UNABLE_TO_VERIFY
        confidence REAL DEFAULT 0.0,
        created_at TEXT NOT NULL,
        FOREIGN KEY (task_id) REFERENCES research_tasks (id)
    )
    """)

    # Research Memory table (Long-term)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS research_memory (
        id TEXT PRIMARY KEY,
        topic TEXT NOT NULL,
        query TEXT NOT NULL,
        findings TEXT NOT NULL, -- JSON list/string
        sources TEXT, -- JSON list
        tags TEXT, -- JSON list
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
