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
    <div className="flex h-full flex-col overflow-hidden rounded-xl border border-blue-100 bg-white shadow-sm">
      {/* Header toolbar */}
      <div className="flex items-center justify-between border-b border-blue-100/80 bg-slate-50 px-4 py-2.5">
        <div className="flex items-center gap-2">
          <Terminal className="h-4 w-4 text-sky-600" />
          <span className="text-xs font-semibold text-slate-700">Sandbox Console Output</span>
          {status === "running" && (
            <span className="flex items-center gap-1.5 text-xs text-sky-700">
              <span className="h-2 w-2 animate-ping rounded-full bg-sky-500" />
              Streaming logs...
            </span>
          )}
        </div>

        <div className="flex items-center gap-2">
          <button
            type="button"
            onClick={handleCopy}
            title="Copy logs"
            className="flex h-7 w-7 items-center justify-center rounded-lg text-slate-600 transition hover:bg-slate-100 hover:text-slate-900"
          >
            {copied ? <Check className="h-3.5 w-3.5 text-sky-600" /> : <Copy className="h-3.5 w-3.5" />}
          </button>
          
          <button
            type="button"
            onClick={onClear}
            title="Clear logs"
            className="flex h-7 w-7 items-center justify-center rounded-lg text-slate-600 transition hover:bg-slate-100 hover:text-red-600"
          >
            <Trash2 className="h-3.5 w-3.5" />
          </button>
        </div>
      </div>

      {/* Log lines viewport */}
      <div className="flex-1 overflow-y-auto p-4 font-mono text-xs leading-6 text-slate-700">
        {logs.length === 0 ? (
          <div className="flex h-full items-center justify-center text-slate-600">
            No execution output yet. Click "Run Plugin" to execute code.
          </div>
        ) : (
          logs.map((log, index) => {
            let textColor = "text-slate-700";
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
