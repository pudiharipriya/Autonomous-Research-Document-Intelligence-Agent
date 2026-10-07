import React from 'react';
import { ShieldCheck, AlertTriangle, XCircle, HelpCircle, FileText, Info } from 'lucide-react';
import { Claim } from '../types';

interface VerificationCardProps {
  claims?: Claim[];
  confidenceScore?: number;
}

export const VerificationCard: React.FC<VerificationCardProps> = ({ claims = [], confidenceScore = 0.0 }) => {
  const safeClaims = Array.isArray(claims) ? claims : [];

  const getStatusBadge = (status: string) => {
    const s = (status || '').toUpperCase();
    switch (s) {
      case 'SUPPORTED':
      case 'VERIFIED':
        return {
          label: 'SUPPORTED',
          icon: ShieldCheck,
          bg: 'bg-emerald-950/40 border-emerald-800/60 text-emerald-400',
        };
      case 'PARTIALLY_SUPPORTED':
        return {
          label: 'PARTIALLY SUPPORTED',
          icon: AlertTriangle,
          bg: 'bg-amber-950/40 border-amber-800/60 text-amber-400',
        };
      case 'CONTRADICTED':
      case 'CONFLICTING':
      case 'UNSUPPORTED':
        return {
          label: 'CONTRADICTED',
          icon: XCircle,
          bg: 'bg-rose-950/40 border-rose-800/60 text-rose-400',
        };
      case 'INSUFFICIENT_EVIDENCE':
      case 'UNABLE_TO_VERIFY':
      default:
        return {
          label: 'INSUFFICIENT EVIDENCE',
          icon: HelpCircle,
          bg: 'bg-slate-900 border-slate-800 text-slate-400',
        };
    }
  };

  return (
    <div className="glass-panel rounded-2xl p-5 border border-slate-800 space-y-4">
      <div className="flex items-center justify-between pb-3 border-b border-slate-800">
        <div className="flex items-center space-x-2">
          <ShieldCheck className="w-5 h-5 text-blue-400" />
          <h3 className="font-semibold text-sm text-white">Fact & Claim Verification Matrix</h3>
        </div>

        <div className="flex items-center space-x-2">
          <span className="text-xs text-slate-400">Mean Confidence:</span>
          <span className="font-mono font-bold text-sm text-blue-400 bg-blue-950/40 px-2 py-0.5 rounded border border-blue-900/60">
            {confidenceScore ?? 0.0}
          </span>
        </div>
      </div>

      <div className="space-y-3">
        {safeClaims.length === 0 ? (
          <p className="text-xs text-slate-400 italic text-center py-4">No claim verification entries available yet.</p>
        ) : (
          safeClaims.map((item: any, idx: number) => {
            const claimText = item.claim_text || item.claim || 'Extracted Research Claim';
            const statusStr = item.verification_status || item.status || 'INSUFFICIENT_EVIDENCE';
            const badge = getStatusBadge(statusStr);
            const Icon = badge.icon;

            return (
              <div key={idx} className="p-4 rounded-xl glass-panel border border-slate-800 space-y-2.5">
                <div className="flex items-start justify-between">
                  <div className="flex items-start space-x-2">
                    <FileText className="w-4 h-4 text-slate-400 shrink-0 mt-0.5" />
                    <h4 className="text-xs font-semibold text-slate-200 leading-snug">{claimText}</h4>
                  </div>

                  <span className={`inline-flex items-center space-x-1 text-[10px] font-mono font-semibold px-2 py-0.5 rounded-full border shrink-0 ml-2 ${badge.bg}`}>
                    <Icon className="w-3 h-3" />
                    <span>{badge.label}</span>
                  </span>
                </div>

                {item.evidence && (
                  <div className="p-2.5 rounded-lg bg-slate-950/80 border border-slate-900 text-[11px] text-slate-300 font-mono">
                    <span className="text-slate-400 font-semibold uppercase text-[9px] block mb-1">Evidence Snippet:</span>
                    <p className="leading-relaxed text-slate-300">"{item.evidence}"</p>
                  </div>
                )}

                {item.reason && (
                  <div className="flex items-start space-x-1.5 text-[11px] text-slate-400 italic pl-1">
                    <Info className="w-3.5 h-3.5 text-blue-400 shrink-0 mt-0.5" />
                    <span>Reasoning: {item.reason}</span>
                  </div>
                )}

                <div className="flex items-center justify-between text-[10px] text-slate-400 pt-1 font-mono border-t border-slate-900">
                  <span>Source: <strong className="text-slate-300">{item.source || 'Uploaded Document'}</strong></span>
                  {item.page && <span>Location: Page {item.page}</span>}
                  <span>Confidence: <strong className="text-blue-400">{item.confidence ?? 0.0}</strong></span>
                </div>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};
