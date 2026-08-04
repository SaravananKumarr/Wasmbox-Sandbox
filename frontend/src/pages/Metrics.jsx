import { useEffect } from "react";
import { Activity, Clock3, CheckCircle2, Cpu } from "lucide-react";
import MetricCard from "../components/metrics/MetricCard";
import ActivityChart from "../components/metrics/ActivityChart";
import RuntimeChart from "../components/metrics/RuntimeChart";
import SuccessRateChart from "../components/metrics/SuccessRateChart";
import ExecutionHistory from "../components/metrics/ExecutionHistory";
import { Card, CardHeader, CardContent } from "../components/common/Card";
import useExecutionStore from "../stores/executionStore";

function Metrics() {
  const { history, metrics, error, fetchHistory, fetchMetrics } = useExecutionStore();

  useEffect(() => {
    fetchHistory();
    fetchMetrics();
  }, [fetchHistory, fetchMetrics]);

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <section>
        <p className="text-sm text-slate-500">Analytics & Performance</p>
        <h2 className="mt-1 text-3xl font-bold tracking-tight text-slate-100">Metrics</h2>
        <p className="mt-2 text-slate-400">
          Monitor WebAssembly runtime performance, execution latency, and success rates.
        </p>
      </section>

      {/* Metric Cards Grid */}
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          title="Total Runs"
          value={metrics?.totalExecutions ?? "--"}
          trend="Recorded"
          subtitle="all sandbox runs"
          icon={Activity}
        />
        <MetricCard
          title="Avg Latency"
          value={metrics ? `${metrics.avgRuntimeMs} ms` : "--"}
          trend="Measured"
          subtitle="all completed runs"
          icon={Clock3}
        />
        <MetricCard
          title="Success Rate"
          value={metrics?.successRate ?? "--"}
          trend="Live"
          subtitle="successful executions"
          icon={CheckCircle2}
        />
        <MetricCard
          title="Peak Memory"
          value={metrics ? `${metrics.peakMemoryMB} MB` : "--"}
          trend={`${metrics?.activeSandboxes ?? 0} active`}
          subtitle="peak observed memory"
          icon={Cpu}
        />
      </section>

      {/* Charts Grid */}
      <section className="grid gap-6 lg:grid-cols-2">
        <Card>
          <CardHeader>
            <div>
              <h3 className="font-semibold text-slate-100">Runtime Duration Trend</h3>
              <p className="mt-1 text-sm text-slate-500">Average vs p95 execution latency (ms)</p>
            </div>
          </CardHeader>
          <CardContent>
            <RuntimeChart history={history} />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <div>
              <h3 className="font-semibold text-slate-100">Execution Status Distribution</h3>
              <p className="mt-1 text-sm text-slate-500">Breakdown of success vs failure causes</p>
            </div>
          </CardHeader>
          <CardContent>
            <SuccessRateChart history={history} />
          </CardContent>
        </Card>
      </section>

      {/* Activity Overview */}
      <Card>
        <CardHeader>
          <div>
            <h3 className="font-semibold text-slate-100">7-Day Execution Volume</h3>
            <p className="mt-1 text-sm text-slate-500">Daily total executions across all multi-tenant sandboxes</p>
          </div>
        </CardHeader>
        <CardContent>
          <ActivityChart history={history} />
        </CardContent>
      </Card>

      {/* Execution History Table */}
      <Card>
        <CardHeader>
          <div>
            <h3 className="font-semibold text-slate-100">Execution History</h3>
            <p className="mt-1 text-sm text-slate-500">Detailed audit trail of recent sandbox invocations</p>
          </div>
        </CardHeader>
        <CardContent>
          <ExecutionHistory history={history} />
        </CardContent>
      </Card>
      {error && <p role="alert" className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">Unable to refresh live metrics: {error}</p>}
    </div>
  );
}

export default Metrics;
