import { useState } from "react";
import * as Tabs from "@radix-ui/react-tabs";
import { Settings as SettingsIcon, Key, Shield, Bell, Check, Save } from "lucide-react";
import { Card, CardContent, CardHeader } from "../components/common/Card";
import Button from "../components/common/Button";
import Badge from "../components/common/Badge";

function Settings() {
  const [saved, setSaved] = useState(false);

  const handleSave = (e) => {
    e.preventDefault();
    setSaved(true);
    setTimeout(() => setSaved(false), 2000);
  };

  return (
    <div className="space-y-8">
      {/* Page Header */}
      <section>
        <p className="text-sm text-slate-500">System Preferences</p>
        <h2 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">Settings</h2>
        <p className="mt-2 text-slate-600">
          Manage tenant configurations, API credentials, and default sandbox settings.
        </p>
      </section>

      {/* Tabs Container */}
      <Tabs.Root defaultValue="general" className="space-y-6">
        <Tabs.List className="flex gap-2 rounded-xl border border-blue-100 bg-slate-50 p-1.5">
          <Tabs.Trigger
            value="general"
            className="flex items-center gap-2 rounded-lg px-4 py-2 text-xs font-medium text-slate-600 transition hover:text-slate-700 data-[state=active]:bg-violet-600 data-[state=active]:text-white"
          >
            <SettingsIcon className="h-4 w-4" /> General
          </Tabs.Trigger>

          <Tabs.Trigger
            value="apikeys"
            className="flex items-center gap-2 rounded-lg px-4 py-2 text-xs font-medium text-slate-600 transition hover:text-slate-700 data-[state=active]:bg-violet-600 data-[state=active]:text-white"
          >
            <Key className="h-4 w-4" /> API Credentials
          </Tabs.Trigger>

          <Tabs.Trigger
            value="policies"
            className="flex items-center gap-2 rounded-lg px-4 py-2 text-xs font-medium text-slate-600 transition hover:text-slate-700 data-[state=active]:bg-violet-600 data-[state=active]:text-white"
          >
            <Shield className="h-4 w-4" /> Default Policies
          </Tabs.Trigger>

          <Tabs.Trigger
            value="notifications"
            className="flex items-center gap-2 rounded-lg px-4 py-2 text-xs font-medium text-slate-600 transition hover:text-slate-700 data-[state=active]:bg-violet-600 data-[state=active]:text-white"
          >
            <Bell className="h-4 w-4" /> Notifications
          </Tabs.Trigger>
        </Tabs.List>

        {/* General Settings Tab */}
        <Tabs.Content value="general">
          <Card>
            <CardHeader>
              <h3 className="font-semibold text-slate-900">Workspace General Settings</h3>
              <p className="text-xs text-slate-600">Configure core developer portal preferences</p>
            </CardHeader>
            <CardContent>
              <form onSubmit={handleSave} className="space-y-5 max-w-xl">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1.5">Workspace Name</label>
                  <input
                    type="text"
                    defaultValue="WasmBox Production Workspace"
                    className="w-full rounded-xl border border-blue-100 bg-slate-50 px-4 py-2.5 text-xs text-slate-700 outline-none focus:border-violet-500/50"
                  />
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1.5">Default WASM Compiler Target</label>
                  <select defaultValue="wasm32-wasi" className="w-full rounded-xl border border-blue-100 bg-slate-50 px-4 py-2.5 text-xs text-slate-700 outline-none focus:border-violet-500/50">
                    <option value="wasm32-wasi">wasm32-wasi (WASI Preview 1/2)</option>
                    <option value="wasm32-unknown-unknown">wasm32-unknown-unknown (Raw WebAssembly)</option>
                  </select>
                </div>

                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1.5">Sandbox Telemetry</label>
                  <p className="text-[11px] text-slate-600 mb-2">Stream detailed nanosecond timing trace logs to observability provider.</p>
                  <div className="flex items-center gap-2">
                    <input type="checkbox" defaultChecked id="telemetry" className="accent-violet-500" />
                    <label htmlFor="telemetry" className="text-xs text-slate-700">Enable OpenTelemetry WASM Traces</label>
                  </div>
                </div>

                <Button type="submit" variant={saved ? "secondary" : "primary"} icon={saved ? Check : Save} size="sm">
                  {saved ? "Settings Saved" : "Save Changes"}
                </Button>
              </form>
            </CardContent>
          </Card>
        </Tabs.Content>

        {/* API Credentials Tab */}
        <Tabs.Content value="apikeys">
          <Card>
            <CardHeader>
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="font-semibold text-slate-900">API Tokens & Webhook Secrets</h3>
                  <p className="text-xs text-slate-500">Access credentials for backend invocation API</p>
                </div>
                <Button size="sm" icon={Key}>Generate New Token</Button>
              </div>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div className="flex items-center justify-between rounded-xl border border-blue-100 bg-slate-50 p-4">
                  <div>
                      <p className="text-xs font-semibold text-slate-700">Production Sandbox Secret Key</p>
                      <code className="mt-1 inline-block font-mono text-xs text-slate-600">wasmbox_live_sk_904128491...841</code>
                  </div>
                  <Badge variant="success">Active</Badge>
                </div>

                <div className="flex items-center justify-between rounded-xl border border-blue-100 bg-slate-50 p-4">
                  <div>
                    <p className="text-xs font-semibold text-slate-700">CLI Deployment Token</p>
                    <code className="mt-1 inline-block font-mono text-xs text-slate-600">wasmbox_cli_tk_29104810...902</code>
                  </div>
                  <Badge variant="neutral">Created 3d ago</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </Tabs.Content>

        {/* Default Policies Tab */}
        <Tabs.Content value="policies">
          <Card>
            <CardHeader>
              <h3 className="font-semibold text-slate-900">Global Security Policy Defaults</h3>
                <p className="text-xs text-slate-600">Base sandbox template applied to newly created plugins</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 max-w-xl">
                <div className="rounded-xl border border-blue-100 bg-slate-50 p-4">
                  <h4 className="text-xs font-semibold text-slate-700">Default Memory Cap</h4>
                  <p className="text-[11px] text-slate-600 mt-1">128 MB maximum memory page size</p>
                </div>
                <div className="rounded-xl border border-blue-100 bg-slate-50 p-4">
                  <h4 className="text-xs font-semibold text-slate-700">Default Execution Timeout</h4>
                  <p className="text-[11px] text-slate-600 mt-1">500 ms CPU wall-clock limit</p>
                </div>
              </div>
            </CardContent>
          </Card>
        </Tabs.Content>

        {/* Notifications Tab */}
        <Tabs.Content value="notifications">
          <Card>
            <CardHeader>
              <h3 className="font-semibold text-slate-900">Alert Webhooks & Notifications</h3>
              <p className="text-xs text-slate-600">Receive alerts when sandbox policy violations occur</p>
            </CardHeader>
            <CardContent>
              <div className="space-y-4 max-w-xl">
                <div>
                  <label className="block text-xs font-medium text-slate-700 mb-1.5">Slack Alert Webhook URL</label>
                  <input
                    type="url"
                    placeholder="https://hooks.slack.com/services/..."
                    className="w-full rounded-xl border border-blue-100 bg-slate-50 px-4 py-2.5 text-xs text-slate-700 outline-none focus:border-violet-500/50"
                  />
                </div>
                <Button size="sm" onClick={handleSave}>Save Notification Rules</Button>
              </div>
            </CardContent>
          </Card>
        </Tabs.Content>
      </Tabs.Root>
    </div>
  );
}

export default Settings;
