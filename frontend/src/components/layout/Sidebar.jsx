import { Code2 } from "lucide-react";

function Sidebar() {
  return (
    <aside className="flex min-h-screen w-60 flex-col border-r border-blue-100 bg-slate-50 p-5">
      <div className="flex items-center gap-3 border-b border-blue-100 pb-5">
        <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-600 font-bold text-white">W</div>
        <div><p className="font-semibold text-slate-900">WasmBox</p><p className="text-xs text-slate-600">Developer Portal</p></div>
      </div>
      <div className="mt-5 flex items-center gap-3 rounded-xl border border-sky-200 bg-sky-100/70 px-3 py-3 text-sm text-slate-900"><Code2 className="h-5 w-5 text-blue-600" /> Editor</div>
    </aside>
  );
}

export default Sidebar;
