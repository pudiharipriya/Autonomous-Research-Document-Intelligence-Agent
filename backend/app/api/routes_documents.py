import os
import uuid
from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from typing import Optional
from app.config import settings
from app.db.models import add_document
from app.tools.document_tool import process_document_tool

router = APIRouter(prefix="/api/documents", tags=["Documents"])

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB

@router.post("/upload")
async def upload_document(
    file: UploadFile = File(...),
    task_id: Optional[str] = Form(None)
):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Invalid file type. Only PDF files are supported.")

    # Sanitize filename to prevent path traversal security risks
    safe_filename = os.path.basename(file.filename)
    doc_id = f"doc_{uuid.uuid4().hex[:8]}"
    file_path = os.path.join(settings.UPLOAD_DIR, f"{doc_id}_{safe_filename}")

    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="File size exceeds maximum limit of 25MB.")

    with open(file_path, "wb") as f:
        f.write(content)

    # Ingest document
    result = process_document_tool(file_path, doc_id)
    if result.get("status") != "success":
        raise HTTPException(status_code=400, detail=result.get("error", "Failed to process PDF."))

    doc_entry = add_document(
        doc_id=doc_id,
        task_id=task_id,
        filename=safe_filename,
        file_path=file_path,
        file_size=len(content),
        page_count=result.get("page_count", 1),
        metadata=result
    )

    return {
        "status": "success",
        "document_id": doc_id,
        "filename": safe_filename,
        "file_path": file_path,
        "file_size": len(content),
        "page_count": result.get("page_count", 1),
        "chunks_indexed": result.get("chunks_indexed", 0)
    }
