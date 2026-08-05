import { Terminal, Trash2, Copy, Check } from "lucide-react";
import { useState } from "react";

function Console({ logs = [], onClear, status = "idle" }) {
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    const fullLogText = logs.join("\n");
    navigator.clipboard.writeText(fullLogText);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex h-full flex-col overflow-hidden rounded-xl border border-slate-800 bg-[#070912]">
      {/* Header toolbar */}
      <div className="flex items-center justify-between border-b border-slate-800/80 bg-[#0b0e19] px-4 py-2.5">
        <div className="flex items-center gap-2">
          <Terminal className="h-4 w-4 text-violet-400" />
          <span className="text-xs font-semibold text-slate-200">Sandbox Console Output</span>
          {status === "running" && (
            <span className="flex items-center gap-1.5 text-xs text-amber-400">
              <span className="h-2 w-2 animate-ping rounded-full bg-amber-400" />
              Streaming logs...
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleCopy}
            title="Copy logs"
            className="flex h-7 w-7 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-800 hover:text-slate-200"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-emerald-400" /> : <Copy className="h-3.5 w-3.5" />}
          </button>
          
          <button
            type="button"
            onClick={onClear}
            title="Clear logs"
            className="flex h-7 w-7 items-center justify-center rounded-lg text-slate-400 transition hover:bg-slate-800 hover:text-red-400"
          >
            <Trash2 className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      {/* Log lines viewport */}
      <div className="flex-1 overflow-y-auto p-4 font-mono text-xs leading-6 text-slate-300">
        {logs.length === 0 ? (
          <div className="flex h-full items-center justify-center text-slate-600">
            No execution output yet. Click "Run Plugin" to execute code.
          </div>
        ) : (
          logs.map((log, index) => {
            let textColor = "text-slate-300";
            if (log.includes("[ERROR]") || log.includes("[FATAL]")) textColor = "text-red-400";
            else if (log.includes("[WARN]")) textColor = "text-amber-400";
            else if (log.includes("[INFO]")) textColor = "text-cyan-400";
            else if (log.includes("[LOG]")) textColor = "text-emerald-300 font-semibold";
            else if (log.includes("[STATUS]")) textColor = "text-violet-400 font-semibold";

            return (
              <div key={index} className={`whitespace-pre-wrap ${textColor}`}>
                {log}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default Console;
