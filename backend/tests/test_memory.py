from app.memory.memory_store import global_memory_store
from app.db.database import init_db

def test_memory_store_operations():
    init_db()
    global_memory_store.clear_all_memory()

    m = global_memory_store.add_memory(
        topic="Transformer Benchmarks",
        query="Transformer BLEU score",
        findings=["Achieves 28.4 BLEU"],
        sources=["https://arxiv.org/abs/1706.03762"],
        tags=["test"]
    )
    assert m["id"] is not None

    memories = global_memory_store.list_memories()
    assert len(memories) >= 1

    searched = global_memory_store.search_memory("Transformer")
    assert len(searched) >= 1

    global_memory_store.clear_all_memory()
    assert len(global_memory_store.list_memories()) == 0
