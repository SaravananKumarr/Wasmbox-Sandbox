import { useEffect, useMemo, useState } from 'react';

type Policy = {
  tenantId: string;
  displayName: string;
  allowedImports: string[];
  maxMemoryPages: number;
  allowNetwork: boolean;
  requireSignedPlugins: boolean;
  maxExecutionTimeMs: number;
  allowedHosts: string[];
  riskLevel: string;
};

type ValidationResult = {
  pluginName: string;
  tenantId: string;
  valid: boolean;
  violations: string[];
  score: number;
  riskLevel: string;
};

type AuditEntry = {
  id: string;
  tenantId: string;
  pluginName: string;
  timestamp: string;
  valid: boolean;
  violations: string[];
};

const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:4000';

export default function App() {
  const [tenantId, setTenantId] = useState('alpha');
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [policy, setPolicy] = useState<Policy | null>(null);
  const [auditEntries, setAuditEntries] = useState<AuditEntry[]>([]);
  const [status, setStatus] = useState('Loading policy…');
  const [pluginName, setPluginName] = useState('sample-plugin');
  const [importsText, setImportsText] = useState('console,env');
  const [memoryPages, setMemoryPages] = useState(24);
  const [network, setNetwork] = useState(false);
  const [signed, setSigned] = useState(true);
  const [executionTimeMs, setExecutionTimeMs] = useState(800);
  const [host, setHost] = useState('');
  const [validation, setValidation] = useState<ValidationResult | null>(null);

  useEffect(() => {
    fetch(`${apiUrl}/tenants`)
      .then((res) => res.json())
      .then((data) => {
        setPolicies(data);
        const first = data[0];
        if (first) {
          setTenantId(first.tenantId);
          setPolicy(first);
        }
      })
      .catch(() => setStatus('Unable to reach API'));
  }, []);

  useEffect(() => {
    if (!tenantId) return;
    fetch(`${apiUrl}/tenants/${tenantId}/policy`)
      .then((res) => res.json())
      .then((data) => {
        setPolicy(data);
        setStatus('Policy loaded successfully');
      })
      .catch(() => setStatus('Unable to reach API'));

    fetch(`${apiUrl}/tenants/${tenantId}/audit`)
      .then((res) => res.json())
      .then((data) => {
        setAuditEntries(data);
      })
      .catch(() => undefined);
  }, [tenantId]);

  const summary = useMemo(() => {
    if (!policy) return [] as string[];
    return [
      `Allowed imports: ${policy.allowedImports.join(', ')}`,
      `Max memory pages: ${policy.maxMemoryPages}`,
      `Network allowed: ${policy.allowNetwork ? 'yes' : 'no'}`,
      `Signed plugins required: ${policy.requireSignedPlugins ? 'yes' : 'no'}`,
      `Max execution time: ${policy.maxExecutionTimeMs} ms`,
      `Allowed hosts: ${policy.allowedHosts.length > 0 ? policy.allowedHosts.join(', ') : 'none'}`,
    ];
  }, [policy]);

  const handleValidate = async () => {
    const payload = {
      pluginName,
      imports: importsText
        .split(',')
        .map((item: string) => item.trim())
        .filter((item: string) => Boolean(item)),
      memoryPages,
      network,
      signed,
      executionTimeMs,
      host,
    };

    const response = await fetch(`${apiUrl}/tenants/${tenantId}/validate`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    const data = await response.json();
    setValidation(data);
    setStatus(data.valid ? 'Plugin passed validation' : 'Plugin rejected');
  };

  return (
    <main style={{ fontFamily: 'Inter, sans-serif', padding: 24, maxWidth: 1200, margin: '0 auto', color: '#0f172a', background: '#f8fafc', minHeight: '100vh' }}>
      <h1 style={{ marginBottom: 8 }}>WasmBox Control Center</h1>
      <p style={{ color: '#475569', lineHeight: 1.6, marginTop: 0 }}>
        Advanced multi-tenant WebAssembly sandboxing with policy enforcement, runtime checks, and audit logging.
      </p>

      <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: 16, marginTop: 24 }}>
        {policies.map((entry) => (
          <button
            key={entry.tenantId}
            onClick={() => setTenantId(entry.tenantId)}
            style={{ textAlign: 'left', padding: 16, borderRadius: 14, border: tenantId === entry.tenantId ? '2px solid #2563eb' : '1px solid #dbe4f0', background: '#fff', cursor: 'pointer' }}
          >
            <strong>{entry.displayName}</strong>
            <div style={{ color: '#64748b', marginTop: 6, fontSize: 13 }}>Risk: {entry.riskLevel}</div>
            <div style={{ color: '#64748b', fontSize: 13 }}>Tenant: {entry.tenantId}</div>
          </button>
        ))}
      </section>

      <section style={{ marginTop: 24, display: 'grid', gap: 24, gridTemplateColumns: '1.1fr 0.9fr' }}>
        <div style={{ padding: 20, borderRadius: 16, background: '#0f172a', color: 'white', boxShadow: '0 12px 30px rgba(15, 23, 42, 0.15)' }}>
          <h2 style={{ marginTop: 0 }}>Tenant policy</h2>
          {policy ? (
            <>
              <p style={{ color: '#cbd5e1' }}>{policy.displayName}</p>
              <ul>
                {summary.map((item) => (
                  <li key={item} style={{ marginBottom: 8 }}>{item}</li>
                ))}
              </ul>
            </>
          ) : (
            <p>{status}</p>
          )}
        </div>

        <div style={{ padding: 20, borderRadius: 16, border: '1px solid #dbe4f0', background: '#fff' }}>
          <h3 style={{ marginTop: 0 }}>Evaluate plugin</h3>
          <div style={{ display: 'grid', gap: 12 }}>
            <input value={pluginName} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setPluginName(e.target.value)} placeholder="Plugin name" style={{ padding: 10, borderRadius: 8, border: '1px solid #cbd5e1' }} />
            <input value={importsText} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setImportsText(e.target.value)} placeholder="Imports (comma separated)" style={{ padding: 10, borderRadius: 8, border: '1px solid #cbd5e1' }} />
            <input type="number" value={memoryPages} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setMemoryPages(Number(e.target.value))} placeholder="Memory pages" style={{ padding: 10, borderRadius: 8, border: '1px solid #cbd5e1' }} />
            <input type="number" value={executionTimeMs} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setExecutionTimeMs(Number(e.target.value))} placeholder="Execution time ms" style={{ padding: 10, borderRadius: 8, border: '1px solid #cbd5e1' }} />
            <input value={host} onChange={(e: React.ChangeEvent<HTMLInputElement>) => setHost(e.target.value)} placeholder="Host" style={{ padding: 10, borderRadius: 8, border: '1px solid #cbd5e1' }} />
            <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <input type="checkbox" checked={network} onChange={() => setNetwork((prev) => !prev)} />
              Allow network
            </label>
            <label style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <input type="checkbox" checked={signed} onChange={() => setSigned((prev) => !prev)} />
              Signed plugin
            </label>
            <button onClick={handleValidate} style={{ padding: 10, borderRadius: 8, background: '#2563eb', color: 'white', border: 'none', cursor: 'pointer' }}>Run validation</button>
            <p style={{ color: '#475569', margin: 0 }}>{status}</p>
          </div>
        </div>
      </section>

      {validation && (
        <section style={{ marginTop: 24, padding: 20, borderRadius: 16, background: '#fff', border: '1px solid #dbe4f0' }}>
          <h3 style={{ marginTop: 0 }}>Validation result</h3>
          <p><strong>Plugin:</strong> {validation.pluginName}</p>
          <p><strong>Status:</strong> {validation.valid ? 'Approved' : 'Rejected'}</p>
          <p><strong>Score:</strong> {validation.score}/100</p>
          <p><strong>Risk:</strong> {validation.riskLevel}</p>
          {validation.violations.length > 0 ? (
            <ul>
              {validation.violations.map((item) => (
                <li key={item}>{item}</li>
              ))}
            </ul>
          ) : (
            <p>No violations detected.</p>
          )}
        </section>
      )}

      <section style={{ marginTop: 24, padding: 20, borderRadius: 16, background: '#fff', border: '1px solid #dbe4f0' }}>
        <h3 style={{ marginTop: 0 }}>Audit trail</h3>
        {auditEntries.length > 0 ? (
          <ul>
            {auditEntries.map((entry) => (
              <li key={entry.id} style={{ marginBottom: 10 }}>
                <strong>{entry.pluginName}</strong> — {entry.valid ? 'approved' : 'rejected'} at {entry.timestamp}
                {entry.violations.length > 0 && <div style={{ color: '#64748b' }}>{entry.violations.join(' | ')}</div>}
              </li>
            ))}
          </ul>
        ) : (
          <p>No audit entries yet.</p>
        )}
      </section>
    </main>
  );
}
