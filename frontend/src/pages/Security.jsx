import { useEffect, useState } from "react";
import SandboxStatus from "../components/security/SandboxStatus";
import PermissionCard from "../components/security/PermissionCard";
import ResourceLimits from "../components/security/ResourceLimits";

import securityService from "../services/securityService";

function Security() {
  const [policy, setPolicy] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => { securityService.getPolicy().then(setPolicy).catch((err) => setError(err.message)); }, []);
  return (
    <div className="space-y-8">
      {/* Page Header */}
      <section>
        <p className="text-sm text-slate-500">Security & Governance</p>
        <h2 className="mt-1 text-3xl font-bold tracking-tight text-slate-100">Sandbox Policies</h2>
        <p className="mt-2 text-slate-400">
          Review the effective isolation policy and resource quotas for plugin execution.
        </p>
      </section>

      {/* Engine Status Banner */}
      {error && <p role="alert" className="rounded-xl border border-red-500/30 bg-red-500/10 px-4 py-3 text-sm text-red-300">Unable to load security policy: {error}</p>}
      <SandboxStatus policy={policy} />

      {/* WASI Capability Grants */}
      <PermissionCard policy={policy} />

      {/* Resource Budgets & Quotas */}
      <ResourceLimits policy={policy} />
    </div>
  );
}

export default Security;
