import { useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { Activity, Blocks, CheckCircle2, Clock3 } from "lucide-react";
import MetricCard from "../components/metrics/MetricCard";
import ActivityChart from "../components/metrics/ActivityChart";
import { Card, CardContent, CardHeader } from "../components/common/Card";
import Badge from "../components/common/Badge";
import usePluginStore from "../stores/pluginStore";
import useExecutionStore from "../stores/executionStore";

function Dashboard() {
  const navigate = useNavigate();
  const { plugins, error: pluginError, fetchPlugins } = usePluginStore();
  const { history, metrics, error: executionError, fetchHistory, fetchMetrics } = useExecutionStore();

  useEffect(() => {
    fetchPlugins();
    fetchHistory();
    fetchMetrics();
  }, [fetchPlugins, fetchHistory, fetchMetrics]);

  const recentPlugins = plugins.slice(0, 3);
  const recentHistory = history.slice(0, 3);
  const error = pluginError || executionError;

  return (
    <div className="space-y-8">
      <section><p className="text-sm text-slate-500">Overview</p><h2 className="mt-1 text-3xl font-bold tracking-tight text-slate-100">Dashboard</h2><p className="mt-2 text-slate-400">Monitor your plugins, executions, and sandbox activity.</p></section>
      {error && <p role="alert" className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">Live data is unavailable: {error}</p>}

      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard title="Total Plugins" value={plugins.length} trend="Saved" subtitle="in this workspace" icon={Blocks} />
        <MetricCard title="Executions" value={metrics?.totalExecutions ?? "--"} trend="Recorded" subtitle="all sandbox runs" icon={Activity} />
        <MetricCard title="Success Rate" value={metrics?.successRate ?? "--"} trend="Live" subtitle="successful runs" icon={CheckCircle2} />
        <MetricCard title="Avg Runtime" value={metrics ? `${metrics.avgRuntimeMs} ms` : "--"} trend="Measured" subtitle="all completed runs" icon={Clock3} />
      </section>

      <section className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <Card><CardHeader><div><h3 className="font-semibold text-slate-100">Execution Activity</h3><p className="mt-1 text-sm text-slate-500">Execution volume over the last 7 days</p></div></CardHeader><CardContent><ActivityChart history={history} /></CardContent></Card>
        <Card><CardHeader><h3 className="font-semibold text-slate-100">Recent Activity</h3></CardHeader><CardContent className="space-y-5">
          {recentHistory.length ? recentHistory.map((item) => <div key={item.id} className="flex gap-3"><div className={`mt-1 h-2 w-2 rounded-full ${item.status === "Success" ? "bg-emerald-400" : "bg-red-400"}`} /><div><p className="text-sm text-slate-300">{item.pluginName} {item.status === "Success" ? "executed successfully" : "failed"}</p><p className="mt-1 text-xs text-slate-500">{item.timestamp}</p></div></div>) : <p className="text-sm text-slate-500">No executions recorded yet.</p>}
        </CardContent></Card>
      </section>

      <Card><CardHeader><div className="flex items-center justify-between gap-4"><div><h3 className="font-semibold text-slate-100">Recent Plugins</h3><p className="mt-1 text-sm text-slate-500">Recently created and executed plugins</p></div><button type="button" onClick={() => navigate("/plugins")} className="text-sm font-medium text-violet-400 transition hover:text-violet-300">View all</button></div></CardHeader><CardContent className="p-0"><div className="overflow-x-auto"><table className="w-full"><thead className="border-b border-slate-800/80"><tr className="text-left text-xs text-slate-500"><th className="px-5 py-3 font-medium">Plugin</th><th className="px-5 py-3 font-medium">Status</th><th className="px-5 py-3 font-medium">Runtime</th><th className="px-5 py-3 font-medium">Updated</th></tr></thead><tbody>
        {recentPlugins.length ? recentPlugins.map((plugin) => <tr key={plugin.id} className="border-b border-slate-800/60 transition last:border-b-0 hover:bg-slate-900/60"><td className="px-5 py-4 text-sm font-medium text-slate-200">{plugin.name}</td><td className="px-5 py-4"><Badge variant={plugin.status === "Active" ? "success" : "warning"}>{plugin.status}</Badge></td><td className="px-5 py-4 font-mono text-sm text-slate-400">{plugin.runtime}</td><td className="px-5 py-4 text-sm text-slate-500">{plugin.updated}</td></tr>) : <tr><td colSpan="4" className="px-5 py-8 text-center text-sm text-slate-500">No plugins created yet.</td></tr>}
      </tbody></table></div></CardContent></Card>
    </div>
  );
}

export default Dashboard;
