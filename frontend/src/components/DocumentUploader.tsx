import React, { useState } from 'react';
import { UploadCloud, FileText, CheckCircle2, AlertCircle, Loader2 } from 'lucide-react';
import { uploadDocument } from '../services/api';

interface DocumentUploaderProps {
  onDocumentUploaded: (docMetadata: any) => void;
}

export const DocumentUploader: React.FC<DocumentUploaderProps> = ({ onDocumentUploaded }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [uploadedDoc, setUploadedDoc] = useState<any | null>(null);

  const handleFileChange = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (!file) return;

    if (!file.name.toLowerCase().endsWith('.pdf')) {
      setError('Only PDF files are supported.');
      return;
    }

    setLoading(true);
    setError(null);

    try {
      const res = await uploadDocument(file);
      setUploadedDoc(res);
      onDocumentUploaded(res);
    } catch (err: any) {
      setError(err.message || 'Failed to upload PDF.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
      <h3 className="font-semibold text-sm text-white flex items-center space-x-2">
        <FileText className="w-4 h-4 text-blue-400" />
        <span>Attach PDF Document (Optional)</span>
      </h3>

      {uploadedDoc ? (
        <div className="p-4 rounded-xl bg-emerald-950/20 border border-emerald-800/40 flex items-center justify-between">
          <div className="flex items-center space-x-3">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <div>
              <p className="text-xs font-semibold text-white">{uploadedDoc.filename}</p>
              <p className="text-[11px] text-slate-400">
                {uploadedDoc.page_count} pages • {uploadedDoc.chunks_indexed} chunks indexed in vector store
              </p>
            </div>
          </div>
          <button
            onClick={() => {
              setUploadedDoc(null);
              onDocumentUploaded(null);
            }}
            className="text-xs text-rose-400 hover:underline"
          >
            Remove
          </button>
        </div>
      ) : (
        <label className="border-2 border-dashed border-slate-800 hover:border-blue-500/50 rounded-xl p-6 flex flex-col items-center justify-center cursor-pointer transition-all bg-slate-950/40">
          {loading ? (
            <div className="flex flex-col items-center space-y-2 text-blue-400">
              <Loader2 className="w-8 h-8 animate-spin" />
              <span className="text-xs font-medium">Extracting PDF text & indexing chunks...</span>
            </div>
          ) : (
            <div className="flex flex-col items-center space-y-2 text-slate-400 hover:text-slate-200">
              <UploadCloud className="w-8 h-8 text-blue-400" />
              <span className="text-xs font-medium text-slate-300">Click or Drag & Drop PDF research paper</span>
              <span className="text-[10px] text-slate-500">Max size: 25MB • Page-level metadata preserved</span>
            </div>
          )}
          <input type="file" accept=".pdf" onChange={handleFileChange} className="hidden" disabled={loading} />
        </label>
      )}

      {error && (
        <div className="p-3 rounded-lg bg-rose-950/30 border border-rose-900/50 flex items-center space-x-2 text-xs text-rose-300">
          <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />
          <span>{error}</span>
        </div>
      )}
    </div>
  );
};
