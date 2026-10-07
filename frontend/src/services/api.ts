import { Task, MemoryItem, ExecutionEvent } from '../types';

const API_BASE = '/api';

export async function checkHealth() {
  const res = await fetch(`${API_BASE}/health`);
  return res.json();
}

export async function uploadDocument(file: File): Promise<{
  document_id: string;
  filename: string;
  file_path: string;
  page_count: number;
  chunks_indexed: number;
}> {
  const formData = new FormData();
  formData.append('file', file);
  const res = await fetch(`${API_BASE}/documents/upload`, {
    method: 'POST',
    body: formData,
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Document upload failed.');
  }
  return res.json();
}

export async function createResearchTask(
  query: string,
  docMetadata: any[] = []
): Promise<{ task_id: string; status: string }> {
  const res = await fetch(`${API_BASE}/research`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      user_query: query,
      document_metadata: docMetadata,
    }),
  });
  if (!res.ok) {
    const err = await res.json();
    throw new Error(err.detail || 'Failed to launch research task.');
  }
  return res.json();
}

export async function getTaskDetails(taskId: string): Promise<Task> {
  const res = await fetch(`${API_BASE}/research/${taskId}`);
  if (!res.ok) {
    throw new Error('Failed to fetch task details.');
  }
  return res.json();
}

export async function listAllTasks(): Promise<Task[]> {
  const res = await fetch(`${API_BASE}/research`);
  if (!res.ok) {
    throw new Error('Failed to fetch research tasks history.');
  }
  return res.json();
}

export async function getMemories(search?: string): Promise<MemoryItem[]> {
  const url = search ? `${API_BASE}/memory?search=${encodeURIComponent(search)}` : `${API_BASE}/memory`;
  const res = await fetch(url);
  if (!res.ok) {
    throw new Error('Failed to fetch memories.');
  }
  return res.json();
}

export async function clearAllMemories(): Promise<void> {
  await fetch(`${API_BASE}/memory`, { method: 'DELETE' });
}

export async function deleteMemory(memoryId: string): Promise<void> {
  await fetch(`${API_BASE}/memory/${memoryId}`, { method: 'DELETE' });
}
