import { Play, Save, Code, CheckCircle, AlertCircle } from "lucide-react";
import Button from "../common/Button";
import Badge from "../common/Badge";

function EditorToolbar({
  pluginName = "untitled.py",
  language = "python",
  onLanguageChange,
  onSave,
  onRun,
  saving = false,
  executionStatus = "idle", // 'idle' | 'running' | 'success' | 'failed'
}) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-slate-800 bg-[#0d111c] px-5 py-3 shadow-lg">
      {/* Plugin details */}
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg border border-violet-500/20 bg-violet-500/10 text-violet-400">
          <Code className="h-5 w-5" />
        </div>
        <div>
          <div className="flex items-center gap-2">
            <h3 className="font-semibold text-slate-100">{pluginName}</h3>
            {executionStatus === "success" && (
              <Badge variant="success" className="gap-1">
                <CheckCircle className="h-3 w-3" /> Success
              </Badge>
            )}
            {executionStatus === "failed" && (
              <Badge variant="danger" className="gap-1">
                <AlertCircle className="h-3 w-3" /> Failed
              </Badge>
            )}
          </div>
          <p className="text-xs text-slate-500">WasmBox Python Sandbox Environment</p>
        </div>
      </div>

      {/* Actions & Language Selector */}
      <div className="flex items-center gap-3">
        <select
          value={language}
          onChange={(e) => onLanguageChange && onLanguageChange(e.target.value)}
          className="rounded-xl border border-slate-800 bg-slate-900/90 px-3 py-2 text-xs text-slate-300 outline-none transition focus:border-violet-500/50"
        >
          <option value="python">Python (Sandbox)</option>
        </select>

        <Button
          variant="secondary"
          size="sm"
          icon={Save}
          loading={saving}
          onClick={onSave}
        >
          Save
        </Button>

        <Button
          variant="primary"
          size="sm"
          icon={Play}
          loading={executionStatus === "running"}
          onClick={onRun}
        >
          {executionStatus === "running" ? "Running..." : "Run Plugin"}
        </Button>
      </div>
    </div>
  );
}

export default EditorToolbar;
