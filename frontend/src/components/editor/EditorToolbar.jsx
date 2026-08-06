import { Code, Play } from "lucide-react";
import Button from "../common/Button";

function EditorToolbar({ onRun, executionStatus = "idle" }) {
  return (
    <div className="flex flex-wrap items-center justify-between gap-4 rounded-xl border border-blue-100 bg-white px-5 py-3 shadow-sm">
      <div className="flex items-center gap-3">
        <div className="flex h-9 w-9 items-center justify-center rounded-lg bg-violet-500/10 text-violet-500"><Code className="h-5 w-5" /></div>
        <div><h3 className="font-semibold text-slate-900">untitled.py</h3><p className="text-xs text-slate-500">Python plugin sandbox</p></div>
      </div>
      <Button variant="primary" size="sm" icon={Play} loading={executionStatus === "running"} onClick={onRun}>
        {executionStatus === "running" ? "Running..." : "Run Plugin"}
      </Button>
    </div>
  );
}

export default EditorToolbar;
