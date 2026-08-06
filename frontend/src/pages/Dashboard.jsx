import {
  Activity,
  Blocks,
  CheckCircle2,
  Clock3,
} from "lucide-react";

import MetricCard from "../components/metrics/MetricCard";
import ActivityChart from "../components/metrics/ActivityChart";

import {
  Card,
  CardContent,
  CardHeader,
} from "../components/common/Card";

import Badge from "../components/common/Badge";

const recentPlugins = [
  {
    name: "customer_formatter.py",
    status: "Active",
    runtime: "18 ms",
    updated: "2 min ago",
  },
  {
    name: "data_validator.py",
    status: "Active",
    runtime: "24 ms",
    updated: "8 min ago",
  },
  {
    name: "webhook_transform.py",
    status: "Draft",
    runtime: "--",
    updated: "21 min ago",
  },
];

function Dashboard() {
  return (
    <div className="space-y-8">
      {/* Page heading */}
      <section>
        <p className="text-sm text-slate-500">
          Overview
        </p>

        <h2 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
          Dashboard
        </h2>

        <p className="mt-2 text-slate-400">
          Monitor your plugins, executions, and sandbox activity.
        </p>
      </section>

      {/* Metric cards */}
      <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
        <MetricCard
          title="Total Plugins"
          value="12"
          trend="+2"
          subtitle="this week"
          icon={Blocks}
        />

        <MetricCard
          title="Executions"
          value="1,284"
          trend="+14%"
          subtitle="from last week"
          icon={Activity}
        />

        <MetricCard
          title="Success Rate"
          value="98.7%"
          trend="Healthy"
          subtitle="sandbox runs"
          icon={CheckCircle2}
        />

        <MetricCard
          title="Avg Runtime"
          value="18.4 ms"
          trend="-3.1%"
          trendType="positive"
          subtitle="faster"
          icon={Clock3}
        />
      </section>

      {/* Chart and recent activity */}
      <section className="grid gap-6 xl:grid-cols-[1.4fr_1fr]">
        <Card>
          <CardHeader>
            <div>
              <h3 className="font-semibold text-slate-900">
                Execution Activity
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                Plugin execution activity over the last 7 days
              </p>
            </div>
          </CardHeader>

          <CardContent>
            <ActivityChart />
          </CardContent>
        </Card>

        <Card>
          <CardHeader>
            <h3 className="font-semibold text-slate-900">
              Recent Activity
            </h3>
          </CardHeader>

          <CardContent className="space-y-5">
            <div className="flex gap-3">
              <div className="mt-1 h-2 w-2 rounded-full bg-emerald-400" />

              <div>
                <p className="text-sm text-slate-700">
                  customer_formatter.py executed successfully
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  2 minutes ago
                </p>
              </div>
            </div>

            <div className="flex gap-3">
              <div className="mt-1 h-2 w-2 rounded-full bg-violet-400" />

              <div>
                <p className="text-sm text-slate-700">
                  New plugin created
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  14 minutes ago
                </p>
              </div>
            </div>

            <div className="flex gap-3">
              <div className="mt-1 h-2 w-2 rounded-full bg-cyan-400" />

              <div>
                <p className="text-sm text-slate-700">
                  Sandbox resource limits updated
                </p>

                <p className="mt-1 text-xs text-slate-500">
                  41 minutes ago
                </p>
              </div>
            </div>
          </CardContent>
        </Card>
      </section>

      {/* Recent plugins */}
      <Card>
        <CardHeader>
          <div className="flex items-center justify-between gap-4">
            <div>
              <h3 className="font-semibold text-slate-900">
                Recent Plugins
              </h3>

              <p className="mt-1 text-sm text-slate-500">
                Recently created and executed plugins
              </p>
            </div>

            <button
              type="button"
              className="
                text-sm
                font-medium
                text-violet-400
                transition
                hover:text-violet-300
              "
            >
              View all
            </button>
          </div>
        </CardHeader>

        <CardContent className="p-0">
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead className="border-b border-blue-100/80">
                <tr className="text-left text-xs text-slate-600">
                  <th className="px-5 py-3 font-medium">
                    Plugin
                  </th>

                  <th className="px-5 py-3 font-medium">
                    Status
                  </th>

                  <th className="px-5 py-3 font-medium">
                    Runtime
                  </th>

                  <th className="px-5 py-3 font-medium">
                    Updated
                  </th>
                </tr>
              </thead>

              <tbody>
                {recentPlugins.map((plugin) => (
                    <tr
                      key={plugin.name}
                      className="
                        border-b
                        border-blue-100/60
                        transition
                        last:border-b-0
                        hover:bg-slate-50
                      "
                    >
                      <td className="px-5 py-4 text-sm font-medium text-slate-900">
                      {plugin.name}
                      </td>

                    <td className="px-5 py-4">
                      <Badge
                        variant={
                          plugin.status === "Active"
                            ? "success"
                            : "warning"
                        }
                      >
                        {plugin.status}
                      </Badge>
                    </td>

                    <td className="px-5 py-4 font-mono text-sm text-slate-700">
                      {plugin.runtime}
                    </td>

                    <td className="px-5 py-4 text-sm text-slate-500">
                      {plugin.updated}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}

export default Dashboard;