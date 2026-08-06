import SandboxStatus from "../components/security/SandboxStatus";
import PermissionCard from "../components/security/PermissionCard";
import ResourceLimits from "../components/security/ResourceLimits";

function Security() {
  return (
    <div className="space-y-8">
      {/* Page Header */}
      <section>
        <p className="text-sm text-slate-500">Security & Governance</p>
        <h2 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">Sandbox Policies</h2>
        <p className="mt-2 text-slate-400">
          Manage WebAssembly isolation, WASI capabilities, and resource quotas for multi-tenant code execution.
        </p>
      </section>

      {/* Engine Status Banner */}
      <SandboxStatus />

      {/* WASI Capability Grants */}
      <PermissionCard />

      {/* Resource Budgets & Quotas */}
      <ResourceLimits />
    </div>
  );
}

export default Security;
