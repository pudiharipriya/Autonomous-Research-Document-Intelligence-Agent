import sys
import os
import asyncio
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "backend"))

from app.db.database import init_db
from app.db.models import get_claims_by_task, get_task
from app.agents.state import AgentState
from app.agents.graph import research_graph_engine

async def main():
    init_db()
    
    query = "How do Large Language Models reduce hallucinations using Retrieval-Augmented Generation (RAG)? Compare RAG with fine-tuning, explain their advantages and limitations, and verify the key claims using academic research papers. Provide citations and evidence for each major claim."
    
    task_id = f"rag_eval_{uuid.uuid4().hex[:6]}"
    
    state = AgentState(
        task_id=task_id,
        user_query=query,
        uploaded_documents=[]
    )
    
    print(f"Executing Autonomous Research Task ({task_id}) for RAG query...")
    final_state = await research_graph_engine.run(state)
    
    print(f"\nTask Status: {final_state.status}")
    print(f"Overall Confidence Score: {final_state.confidence}")
    print(f"Total Verified Claims Extracted: {len(final_state.verified_claims)}")
    print(f"Total Citations Generated: {len(final_state.citations)}")
    
    print("\n--- Extracted Claims & Verification Results ---")
    for idx, claim in enumerate(final_state.verified_claims, 1):
        print(f"\nClaim [{idx}]: {claim['claim']}")
        print(f"  Verdict: {claim['verification_status']}")
        print(f"  Source: {claim['source']}")
        print(f"  Confidence: {claim['confidence']}")
        print(f"  Evidence: {claim['evidence'][:120]}...")
        
    # Verify DB Persistence
    saved_claims = get_claims_by_task(task_id)
    print(f"\nRetrieved {len(saved_claims)} claim records from SQLite database for task '{task_id}'.")
    assert len(saved_claims) == len(final_state.verified_claims)
    print("[SUCCESS] DB Persistence Verification Passed!")

if __name__ == "__main__":
    asyncio.run(main())
