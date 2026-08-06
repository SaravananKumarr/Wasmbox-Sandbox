import { useState } from "react";
import * as Switch from "@radix-ui/react-switch";
import { HardDrive, Globe, Terminal, FileCode2 } from "lucide-react";
import { Card, CardContent, CardHeader } from "../common/Card";
import Badge from "../common/Badge";

const defaultPermissions = [
  {
    id: "wasi_fs",
    title: "WASI Filesystem Access",
    description: "Restrict guest plugin access to virtual read-only sandbox directories.",
    icon: HardDrive,
    enabled: true,
    capability: "wasi:filesystem/read",
  },
  {
    id: "outgoing_http",
    title: "Outgoing HTTP / Sockets",
    description: "Allow plugins to issue external HTTP requests via host proxy.",
    icon: Globe,
    enabled: false,
    capability: "wasi:sockets/outbound",
  },
  {
    id: "env_vars",
    title: "Environment Variable Access",
    description: "Expose tenant configuration key-values to guest WASM context.",
    icon: Terminal,
    enabled: true,
    capability: "wasi:cli/environment",
  },
  {
    id: "host_imports",
    title: "Custom Host Functions",
    description: "Import host system utilities into WebAssembly instance memory.",
    icon: FileCode2,
    enabled: true,
    capability: "wasmbox:host_bindings",
  },
];

function PermissionCard() {
  const [permissions, setPermissions] = useState(defaultPermissions);

  const togglePermission = (id) => {
    setPermissions((prev) =>
      prev.map((p) => (p.id === id ? { ...p, enabled: !p.enabled } : p))
    );
  };

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <div>
            <h3 className="font-semibold text-slate-900">Sandbox Capabilities & Permissions</h3>
            <p className="mt-1 text-sm text-slate-600">
              Configure strict capability grants for multi-tenant plugin executions.
            </p>
          </div>
          <Badge variant="neutral">WASI 0.2 Standard</Badge>
        </div>
      </CardHeader>
      <CardContent>
        <div className="grid gap-4 md:grid-cols-2">
          {permissions.map((perm) => {
            const Icon = perm.icon;
            return (
              <div
                key={perm.id}
                className="flex items-start justify-between gap-4 rounded-xl border border-blue-100 bg-slate-50 p-4 transition hover:border-blue-200"
              >
                <div className="flex items-start gap-3">
                  <div className="mt-0.5 flex h-9 w-9 shrink-0 items-center justify-center rounded-lg border border-blue-100 bg-slate-50 text-violet-400">
                    <Icon className="h-4 w-4" />
                  </div>
                  <div>
                    <h4 className="text-sm font-semibold text-slate-900">{perm.title}</h4>
                    <p className="mt-1 text-xs text-slate-600 leading-5">{perm.description}</p>
                    <code className="mt-2 inline-block rounded bg-slate-100 px-2 py-0.5 font-mono text-[10px] text-slate-600">
                      {perm.capability}
                    </code>
                  </div>
                </div>

                <Switch.Root
                  checked={perm.enabled}
                  onCheckedChange={() => togglePermission(perm.id)}
                  className={`relative h-6 w-11 shrink-0 rounded-full transition-colors duration-200 ease-in-out focus:outline-none focus:ring-2 focus:ring-violet-500 ${
                    perm.enabled ? "bg-violet-600" : "bg-slate-800"
                  }`}
                >
                  <Switch.Thumb
                    className={`block h-5 w-5 transform rounded-full bg-white shadow-md transition-transform duration-200 ease-in-out ${
                      perm.enabled ? "translate-x-5" : "translate-x-0.5"
                    }`}
                  />
                </Switch.Root>
              </div>
            );
          })}
        </div>
      </CardContent>
    </Card>
  );
}

export default PermissionCard;
