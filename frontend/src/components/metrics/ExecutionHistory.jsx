import { useState } from "react";
import Badge from "../common/Badge";
import { Filter, Search } from "lucide-react";

function ExecutionHistory({ history = [] }) {
  const [filter, setFilter] = useState("all");
  const [search, setSearch] = useState("");

  const filtered = history.filter((item) => {
    const matchesFilter =
      filter === "all" ||
      (filter === "success" && item.status === "Success") ||
      (filter === "failed" && item.status === "Failed");

    const matchesSearch =
      item.pluginName.toLowerCase().includes(search.toLowerCase()) ||
      item.id.toLowerCase().includes(search.toLowerCase());

    return matchesFilter && matchesSearch;
  });

  return (
    <div className="space-y-4">
      {/* Controls */}
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div className="flex items-center gap-2 rounded-xl border border-slate-800 bg-[#0d111c] px-3.5 py-2.5">
          <Search className="h-4 w-4 text-slate-500" />
          <input
            type="text"
            placeholder="Search execution logs..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="bg-transparent text-xs text-slate-200 outline-none placeholder:text-slate-600"
          />
        </div>

        <div className="flex items-center gap-2">
          <Filter className="h-4 w-4 text-slate-500" />
          <div className="flex rounded-xl border border-slate-800 bg-[#0d111c] p-1">
            <button
              type="button"
              onClick={() => setFilter("all")}
              className={`rounded-lg px-3 py-1 text-xs font-medium transition ${
                filter === "all" ? "bg-violet-600 text-white" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              All
            </button>
            <button
              type="button"
              onClick={() => setFilter("success")}
              className={`rounded-lg px-3 py-1 text-xs font-medium transition ${
                filter === "success" ? "bg-emerald-600 text-white" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Success
            </button>
            <button
              type="button"
              onClick={() => setFilter("failed")}
              className={`rounded-lg px-3 py-1 text-xs font-medium transition ${
                filter === "failed" ? "bg-red-600 text-white" : "text-slate-400 hover:text-slate-200"
              }`}
            >
              Failed
            </button>
          </div>
        </div>
      </div>

      {/* History table */}
      <div className="overflow-x-auto rounded-xl border border-slate-800 bg-[#0d111c]">
        <table className="w-full text-left">
          <thead className="border-b border-slate-800/80 bg-slate-900/40 text-xs text-slate-500">
            <tr>
              <th className="px-5 py-3.5 font-medium">Execution ID</th>
              <th className="px-5 py-3.5 font-medium">Plugin</th>
              <th className="px-5 py-3.5 font-medium">Status</th>
              <th className="px-5 py-3.5 font-medium">Latency</th>
              <th className="px-5 py-3.5 font-medium">Memory</th>
              <th className="px-5 py-3.5 font-medium">Executed At</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-800/60 text-xs">
            {filtered.length === 0 ? (
              <tr>
                <td colSpan={6} className="px-5 py-8 text-center text-slate-500">
                  No execution records match the current filter criteria.
                </td>
              </tr>
            ) : (
              filtered.map((item) => (
                <tr key={item.id} className="transition hover:bg-slate-900/50">
                  <td className="px-5 py-4 font-mono font-medium text-violet-400">{item.id}</td>
                  <td className="px-5 py-4 font-medium text-slate-200">{item.pluginName}</td>
                  <td className="px-5 py-4">
                    <Badge variant={item.status === "Success" ? "success" : "danger"}>
                      {item.status}
                    </Badge>
                  </td>
                  <td className="px-5 py-4 font-mono text-slate-400">{item.duration} ms</td>
                  <td className="px-5 py-4 font-mono text-slate-400">{item.memory} MB</td>
                  <td className="px-5 py-4 text-slate-500">{item.timestamp}</td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}

export default ExecutionHistory;
