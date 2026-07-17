import { useEffect, useMemo, useState, type CSSProperties, type ReactNode } from 'react';

type RiskLevel = 'low' | 'medium' | 'high';
type ConnectionState = 'connecting' | 'live' | 'demo';

type Policy = {
  tenantId: string;
  displayName: string;
  allowedImports: string[];
  maxMemoryPages: number;
  allowNetwork: boolean;
  requireSignedPlugins: boolean;
  maxExecutionTimeMs: number;
  allowedHosts: string[];
  riskLevel: RiskLevel;
};

type ValidationResult = {
  pluginName: string;
  tenantId: string;
  valid: boolean;
  violations: string[];
  score: number;
  riskLevel: RiskLevel;
};

type AuditEntry = {
  id: string;
  tenantId: string;
  pluginName: string;
  timestamp: string;
  valid: boolean;
  violations: string[];
};

type CompileResult = {
  tenantId: string;
  pluginName: string;
  wasmBinary: string;
  compiled: boolean;
  message: string;
  executionTimeMs: number;
  memoryBytes: number;
};

type IconName =
  | 'activity'
  | 'bell'
  | 'check'
  | 'chevron'
  | 'clock'
  | 'close'
  | 'code'
  | 'cube'
  | 'dashboard'
  | 'globe'
  | 'history'
  | 'key'
  | 'lock'
  | 'memory'
  | 'menu'
  | 'scan'
  | 'search'
  | 'server'
  | 'settings'
  | 'shield'
  | 'sliders'
  | 'sparkles'
  | 'terminal'
  | 'x';

const ICONS: Record<IconName, ReactNode> = {
  activity: <><path d="M3 12h4l2-7 4 14 2-7h6" /></>,
  bell: <><path d="M18 8a6 6 0 0 0-12 0c0 7-3 7-3 9h18c0-2-3-2-3-9" /><path d="M10 21h4" /></>,
  check: <path d="m5 12 4 4L19 6" />,
  chevron: <path d="m9 18 6-6-6-6" />,
  clock: <><circle cx="12" cy="12" r="9" /><path d="M12 7v5l3 2" /></>,
  close: <><path d="m6 6 12 12" /><path d="m18 6-12 12" /></>,
  code: <><path d="m8 9-3 3 3 3" /><path d="m16 9 3 3-3 3" /><path d="m14 5-4 14" /></>,
  cube: <><path d="m12 3 8 4.5v9L12 21l-8-4.5v-9L12 3Z" /><path d="m4.5 7.8 7.5 4.3 7.5-4.3" /><path d="M12 12v9" /></>,
  dashboard: <><rect x="3" y="3" width="7" height="7" rx="2" /><rect x="14" y="3" width="7" height="7" rx="2" /><rect x="3" y="14" width="7" height="7" rx="2" /><rect x="14" y="14" width="7" height="7" rx="2" /></>,
  globe: <><circle cx="12" cy="12" r="9" /><path d="M3 12h18M12 3a15 15 0 0 1 0 18M12 3a15 15 0 0 0 0 18" /></>,
  history: <><path d="M3 12a9 9 0 1 0 3-6.7L3 8" /><path d="M3 3v5h5M12 7v5l3 2" /></>,
  key: <><circle cx="8" cy="15" r="4" /><path d="m11 12 8-8M15 8l3 3M17 6l2 2" /></>,
  lock: <><rect x="5" y="10" width="14" height="11" rx="2" /><path d="M8 10V7a4 4 0 0 1 8 0v3" /></>,
  memory: <><rect x="4" y="6" width="16" height="12" rx="2" /><path d="M8 10h8M8 14h5M7 3v3M12 3v3M17 3v3M7 18v3M12 18v3M17 18v3" /></>,
  menu: <><path d="M4 7h16M4 12h16M4 17h16" /></>,
  scan: <><path d="M4 7V5a1 1 0 0 1 1-1h2M17 4h2a1 1 0 0 1 1 1v2M20 17v2a1 1 0 0 1-1 1h-2M7 20H5a1 1 0 0 1-1-1v-2" /><path d="m8 12 2.5 2.5L16 9" /></>,
  search: <><circle cx="11" cy="11" r="7" /><path d="m20 20-4-4" /></>,
  server: <><rect x="3" y="4" width="18" height="6" rx="2" /><rect x="3" y="14" width="18" height="6" rx="2" /><path d="M7 7h.01M7 17h.01" /></>,
  settings: <><circle cx="12" cy="12" r="3" /><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6v.2h-4V21a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3 14H2.8v-4H3a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1a1.7 1.7 0 0 0 1.9.3A1.7 1.7 0 0 0 10 3V2.8h4V3a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.2v4H21a1.7 1.7 0 0 0-1.6 1Z" /></>,
  shield: <><path d="M12 3 20 6v5c0 5-3.4 8.6-8 10-4.6-1.4-8-5-8-10V6l8-3Z" /><path d="m8.5 12 2.2 2.2 4.8-5" /></>,
  sliders: <><path d="M4 6h10M18 6h2M4 12h2M10 12h10M4 18h7M15 18h5" /><circle cx="16" cy="6" r="2" /><circle cx="8" cy="12" r="2" /><circle cx="13" cy="18" r="2" /></>,
  sparkles: <><path d="m12 3 1.1 3.4L16.5 7.5l-3.4 1.1L12 12l-1.1-3.4-3.4-1.1 3.4-1.1L12 3Z" /><path d="m18 13 .7 2.3L21 16l-2.3.7L18 19l-.7-2.3L15 16l2.3-.7L18 13ZM6 14l.8 2.2L9 17l-2.2.8L6 20l-.8-2.2L3 17l2.2-.8L6 14Z" /></>,
  terminal: <><rect x="3" y="4" width="18" height="16" rx="2" /><path d="m7 9 3 3-3 3M13 15h4" /></>,
  x: <path d="m7 7 10 10M17 7 7 17" />,
};

function Icon({ name, size = 18 }: { name: IconName; size?: number }) {
  return (
    <svg
      aria-hidden="true"
      className="icon"
      fill="none"
      height={size}
      viewBox="0 0 24 24"
      width={size}
    >
      {ICONS[name]}
    </svg>
  );
}

const FALLBACK_POLICIES: Policy[] = [
  {
    tenantId: 'alpha',
    displayName: 'Alpha Secure Workspace',
    allowedImports: ['console', 'env', 'crypto'],
    maxMemoryPages: 64,
    allowNetwork: false,
    requireSignedPlugins: true,
    maxExecutionTimeMs: 1250,
    allowedHosts: [],
    riskLevel: 'high',
  },
  {
    tenantId: 'beta',
    displayName: 'Beta Innovation Sandbox',
    allowedImports: ['console'],
    maxMemoryPages: 32,
    allowNetwork: true,
    requireSignedPlugins: false,
    maxExecutionTimeMs: 2500,
    allowedHosts: ['api.example.com', 'storage.example.com'],
    riskLevel: 'medium',
  },
  {
    tenantId: 'gamma',
    displayName: 'Gamma Research Lab',
    allowedImports: ['console', 'env', 'fetch'],
    maxMemoryPages: 96,
    allowNetwork: true,
    requireSignedPlugins: false,
    maxExecutionTimeMs: 4000,
    allowedHosts: ['*.example.org', 'localhost'],
    riskLevel: 'low',
  },
];

const now = Date.now();
const FALLBACK_AUDIT: AuditEntry[] = [
  {
    id: 'demo-1',
    tenantId: 'alpha',
    pluginName: 'invoice-parser.wasm',
    timestamp: new Date(now - 4 * 60_000).toISOString(),
    valid: true,
    violations: [],
  },
  {
    id: 'demo-2',
    tenantId: 'alpha',
    pluginName: 'data-exporter.wasm',
    timestamp: new Date(now - 19 * 60_000).toISOString(),
    valid: false,
    violations: ['Network access is not allowed for this tenant'],
  },
  {
    id: 'demo-3',
    tenantId: 'alpha',
    pluginName: 'risk-engine.wasm',
    timestamp: new Date(now - 52 * 60_000).toISOString(),
    valid: true,
    violations: [],
  },
  {
    id: 'demo-4',
    tenantId: 'alpha',
    pluginName: 'legacy-transform.wasm',
    timestamp: new Date(now - 2.2 * 60 * 60_000).toISOString(),
    valid: false,
    violations: ['Plugin must be signed', 'Memory exceeds limit (64 pages)'],
  },
];

const configuredApiUrl = import.meta.env.VITE_API_URL?.replace(/\/$/, '');
const apiUrl = configuredApiUrl || (import.meta.env.DEV ? 'http://localhost:4000' : '');
const defaultSource = `def run(data):
    return f"Hello {data}"`;

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`${apiUrl}${path}`, init);
  const contentType = response.headers.get('content-type') ?? '';

  if (!response.ok || !contentType.includes('application/json')) {
    throw new Error(`Request failed with status ${response.status}`);
  }

  return response.json() as Promise<T>;
}

function evaluateLocally(policy: Policy, payload: {
  pluginName: string;
  imports: string[];
  memoryPages: number;
  network: boolean;
  signed: boolean;
  executionTimeMs: number;
  host: string;
}): ValidationResult {
  const violations: string[] = [];

  if (policy.requireSignedPlugins && !payload.signed) violations.push('Plugin must be signed');

  const disallowedImports = payload.imports.filter((entry) => !policy.allowedImports.includes(entry));
  if (disallowedImports.length) violations.push(`Disallowed imports: ${disallowedImports.join(', ')}`);
  if (payload.memoryPages > policy.maxMemoryPages) violations.push(`Memory exceeds limit (${policy.maxMemoryPages} pages)`);
  if (!policy.allowNetwork && payload.network) violations.push('Network access is not allowed for this tenant');
  if (payload.executionTimeMs > policy.maxExecutionTimeMs) violations.push(`Execution time exceeds limit (${policy.maxExecutionTimeMs} ms)`);
  if (payload.network && payload.host && policy.allowedHosts.length > 0 && !policy.allowedHosts.includes(payload.host)) {
    violations.push(`Host is not in the allowlist: ${payload.host}`);
  }

  return {
    pluginName: payload.pluginName,
    tenantId: policy.tenantId,
    valid: violations.length === 0,
    violations,
    score: Math.max(0, 100 - violations.length * 20),
    riskLevel: policy.riskLevel,
  };
}

function formatRelativeTime(timestamp: string) {
  const minutes = Math.round((new Date(timestamp).getTime() - Date.now()) / 60_000);
  const formatter = new Intl.RelativeTimeFormat('en', { numeric: 'auto' });
  if (Math.abs(minutes) < 60) return formatter.format(minutes, 'minute');
  const hours = Math.round(minutes / 60);
  if (Math.abs(hours) < 24) return formatter.format(hours, 'hour');
  return formatter.format(Math.round(hours / 24), 'day');
}

function getPolicyStrength(policy: Policy | null) {
  if (!policy) return 0;
  let score = 62;
  if (policy.requireSignedPlugins) score += 12;
  if (!policy.allowNetwork) score += 10;
  if (policy.allowedImports.length <= 3) score += 6;
  if (policy.maxExecutionTimeMs <= 1500) score += 5;
  if (policy.maxMemoryPages <= 64) score += 5;
  return Math.min(score, 100);
}

export default function App() {
  const [tenantId, setTenantId] = useState('alpha');
  const [policies, setPolicies] = useState<Policy[]>([]);
  const [policy, setPolicy] = useState<Policy | null>(null);
  const [auditEntries, setAuditEntries] = useState<AuditEntry[]>([]);
  const [connection, setConnection] = useState<ConnectionState>('connecting');
  const [showDemoNotice, setShowDemoNotice] = useState(true);
  const [mobileNavOpen, setMobileNavOpen] = useState(false);
  const [auditSearch, setAuditSearch] = useState('');
  const [pluginName, setPluginName] = useState('payment-guard.wasm');
  const [importsText, setImportsText] = useState('console, env');
  const [memoryPages, setMemoryPages] = useState(24);
  const [network, setNetwork] = useState(false);
  const [signed, setSigned] = useState(true);
  const [executionTimeMs, setExecutionTimeMs] = useState(800);
  const [host, setHost] = useState('');
  const [sourceCode, setSourceCode] = useState(defaultSource);
  const [validation, setValidation] = useState<ValidationResult | null>(null);
  const [validationError, setValidationError] = useState('');
  const [isValidating, setIsValidating] = useState(false);
  const [compileResult, setCompileResult] = useState<CompileResult | null>(null);
  const [isCompiling, setIsCompiling] = useState(false);

  useEffect(() => {
    let cancelled = false;

    async function loadTenants() {
      try {
        const data = await requestJson<Policy[]>('/tenants');
        if (cancelled) return;
        setPolicies(data);
        setTenantId(data[0]?.tenantId ?? 'alpha');
        setConnection('live');
      } catch {
        if (cancelled) return;
        setPolicies(FALLBACK_POLICIES);
        setPolicy(FALLBACK_POLICIES[0]);
        setAuditEntries(FALLBACK_AUDIT);
        setConnection('demo');
      }
    }

    loadTenants();
    return () => {
      cancelled = true;
    };
  }, []);

  useEffect(() => {
    if (!policies.length) return;

    setValidation(null);
    const localPolicy = policies.find((entry) => entry.tenantId === tenantId) ?? policies[0];
    setPolicy(localPolicy);

    if (connection !== 'live') {
      setAuditEntries(FALLBACK_AUDIT.filter((entry) => entry.tenantId === tenantId));
      return;
    }

    let cancelled = false;
    Promise.all([
      requestJson<Policy>(`/tenants/${tenantId}/policy`),
      requestJson<AuditEntry[]>(`/tenants/${tenantId}/audit`),
    ])
      .then(([policyData, auditData]) => {
        if (cancelled) return;
        setPolicy(policyData);
        setAuditEntries(auditData);
      })
      .catch(() => {
        if (cancelled) return;
        setConnection('demo');
        setPolicies(FALLBACK_POLICIES);
        setPolicy(FALLBACK_POLICIES.find((entry) => entry.tenantId === tenantId) ?? FALLBACK_POLICIES[0]);
        setAuditEntries(FALLBACK_AUDIT.filter((entry) => entry.tenantId === tenantId));
      });

    return () => {
      cancelled = true;
    };
  }, [connection, policies, tenantId]);

  const policyStrength = useMemo(() => getPolicyStrength(policy), [policy]);
  const filteredAuditEntries = useMemo(() => {
    const query = auditSearch.trim().toLowerCase();
    if (!query) return auditEntries;
    return auditEntries.filter((entry) =>
      [entry.pluginName, entry.valid ? 'approved' : 'blocked', ...entry.violations]
        .join(' ')
        .toLowerCase()
        .includes(query),
    );
  }, [auditEntries, auditSearch]);

  const controlItems = useMemo(() => {
    if (!policy) return [];
    return [
      { icon: 'key' as IconName, label: 'Signed artifacts', value: policy.requireSignedPlugins ? 'Required' : 'Optional', active: policy.requireSignedPlugins },
      { icon: 'globe' as IconName, label: 'Network isolation', value: policy.allowNetwork ? 'Allowlisted' : 'Isolated', active: true },
      { icon: 'code' as IconName, label: 'Import boundary', value: `${policy.allowedImports.length} imports`, active: true },
      { icon: 'clock' as IconName, label: 'Execution timeout', value: `${(policy.maxExecutionTimeMs / 1000).toFixed(2)} sec`, active: true },
    ];
  }, [policy]);

  async function handleCompile() {
    setIsCompiling(true);
    try {
      const result = await requestJson<CompileResult>('/plugins/compile', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ tenantId, pluginName: pluginName.trim() || 'plugin', sourceCode }),
      });
      setCompileResult(result);
      setValidationError('');
    } catch {
      setCompileResult({
        tenantId,
        pluginName: pluginName.trim() || 'plugin',
        wasmBinary: '',
        compiled: false,
        message: 'Compilation service unavailable. Using local fallback mode.',
        executionTimeMs: 0,
        memoryBytes: 0,
      });
    } finally {
      setIsCompiling(false);
    }
  }

  async function handleValidate() {
    if (!policy || !pluginName.trim()) {
      setValidationError('Enter a plugin name before running validation.');
      return;
    }

    setValidationError('');
    setIsValidating(true);
    const payload = {
      pluginName: pluginName.trim(),
      imports: importsText.split(',').map((entry) => entry.trim()).filter(Boolean),
      memoryPages,
      network,
      signed,
      executionTimeMs,
      host: host.trim(),
    };

    let result: ValidationResult;
    try {
      if (connection !== 'live') throw new Error('Use local evaluator');
      result = await requestJson<ValidationResult>(`/tenants/${tenantId}/validate`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      });
    } catch {
      result = evaluateLocally(policy, payload);
      setConnection('demo');
    } finally {
      setIsValidating(false);
    }

    setValidation(result);
    setAuditEntries((entries) => [
      {
        id: `${result.tenantId}-${Date.now()}`,
        tenantId: result.tenantId,
        pluginName: result.pluginName,
        timestamp: new Date().toISOString(),
        valid: result.valid,
        violations: result.violations,
      },
      ...entries.filter((entry) => entry.pluginName !== result.pluginName),
    ]);
  }

  function closeMobileNavigation() {
    setMobileNavOpen(false);
  }

  return (
    <div className="app-shell">
      <button
        aria-label="Close navigation"
        className={`nav-scrim ${mobileNavOpen ? 'is-visible' : ''}`}
        onClick={closeMobileNavigation}
        type="button"
      />

      <aside className={`sidebar ${mobileNavOpen ? 'is-open' : ''}`}>
        <div className="brand-row">
          <div className="brand-mark"><Icon name="cube" size={22} /></div>
          <div>
            <div className="brand-name">WasmBox</div>
            <div className="brand-edition">Security Cloud</div>
          </div>
          <button aria-label="Close menu" className="sidebar-close" onClick={closeMobileNavigation} type="button">
            <Icon name="close" size={20} />
          </button>
        </div>

        <div className="environment-pill">
          <span className="pulse-dot" />
          <span>Production</span>
          <span className="environment-region">BLR-1</span>
        </div>

        <nav aria-label="Primary navigation" className="primary-nav">
          <div className="nav-label">Workspace</div>
          <a className="nav-link active" href="#overview" onClick={closeMobileNavigation}>
            <Icon name="dashboard" /><span>Overview</span>
          </a>
          <a className="nav-link" href="#policy" onClick={closeMobileNavigation}>
            <Icon name="sliders" /><span>Policy engine</span>
          </a>
          <a className="nav-link" href="#validation" onClick={closeMobileNavigation}>
            <Icon name="scan" /><span>Plugin validation</span>
            <span className="nav-badge">Live</span>
          </a>
          <a className="nav-link" href="#audit" onClick={closeMobileNavigation}>
            <Icon name="history" /><span>Audit log</span>
          </a>

          <div className="nav-label nav-label-spaced">Platform</div>
          <a className="nav-link" href="#runtime" onClick={closeMobileNavigation}>
            <Icon name="server" /><span>Runtime fleet</span>
          </a>
          <a className="nav-link" href="#settings" onClick={closeMobileNavigation}>
            <Icon name="settings" /><span>Configuration</span>
          </a>
        </nav>

        <div className="sidebar-bottom">
          <div className="protection-card">
            <div className="protection-icon"><Icon name="shield" size={18} /></div>
            <div>
              <strong>Protection active</strong>
              <span>All runtime guards enabled</span>
            </div>
          </div>
          <div className="profile-row">
            <div className="avatar">SK</div>
            <div className="profile-copy">
              <strong>Security team</strong>
              <span>Platform admin</span>
            </div>
            <button aria-label="Open profile settings" className="icon-button subtle" type="button">
              <Icon name="chevron" size={16} />
            </button>
          </div>
        </div>
      </aside>

      <main className="workspace">
        <header className="topbar">
          <div className="topbar-left">
            <button aria-label="Open navigation" className="mobile-menu-button" onClick={() => setMobileNavOpen(true)} type="button">
              <Icon name="menu" size={21} />
            </button>
            <div className="breadcrumb"><span>Security operations</span><Icon name="chevron" size={14} /><strong>Overview</strong></div>
          </div>
          <div className="topbar-actions">
            <label className="global-search">
              <Icon name="search" size={17} />
              <input
                aria-label="Search audit events"
                onChange={(event) => setAuditSearch(event.target.value)}
                placeholder="Search events..."
                value={auditSearch}
              />
              <kbd>⌘ K</kbd>
            </label>
            <button aria-label="Notifications" className="icon-button notification-button" type="button">
              <Icon name="bell" size={19} /><span className="notification-dot" />
            </button>
          </div>
        </header>

        <div className="page-content">
          <section className="page-heading" id="overview">
            <div>
              <div className="eyebrow"><span className="eyebrow-line" /> Runtime security</div>
              <h1>WasmBox Developer Portal</h1>
              <p>Enforce tenant boundaries, inspect runtime posture, and validate WebAssembly plugins before execution.</p>
            </div>
            <div className="heading-actions">
              <div className={`connection-badge ${connection}`}>
                <span className="status-dot" />
                {connection === 'live' ? 'API connected' : connection === 'connecting' ? 'Connecting' : 'Demo data'}
              </div>
              <a className="primary-button" href="#validation">
                <Icon name="scan" size={17} /> Validate plugin
              </a>
            </div>
          </section>

          {connection === 'demo' && showDemoNotice && (
            <div className="demo-notice">
              <Icon name="sparkles" size={18} />
              <div><strong>Interactive demo mode</strong><span>Connect your deployed API with <code>VITE_API_URL</code> to use live tenant data.</span></div>
              <button aria-label="Dismiss demo notice" onClick={() => setShowDemoNotice(false)} type="button"><Icon name="close" size={17} /></button>
            </div>
          )}

          <section aria-label="Tenant overview" className="metrics-grid">
            <article className="metric-card">
              <div className="metric-icon violet"><Icon name="server" /></div>
              <div className="metric-copy"><span>Tenant workspaces</span><strong>{policies.length || '—'}</strong></div>
              <span className="metric-foot positive"><Icon name="activity" size={14} /> All operational</span>
            </article>
            <article className="metric-card">
              <div className="metric-icon blue"><Icon name="code" /></div>
              <div className="metric-copy"><span>Allowed imports</span><strong>{policy?.allowedImports.length ?? '—'}</strong></div>
              <span className="metric-foot">Strict allowlist</span>
            </article>
            <article className="metric-card">
              <div className="metric-icon mint"><Icon name="memory" /></div>
              <div className="metric-copy"><span>Memory ceiling</span><strong>{policy ? `${policy.maxMemoryPages * 64} KiB` : '—'}</strong></div>
              <span className="metric-foot">Per instance</span>
            </article>
            <article className="metric-card">
              <div className="metric-icon amber"><Icon name="clock" /></div>
              <div className="metric-copy"><span>Runtime timeout</span><strong>{policy ? `${(policy.maxExecutionTimeMs / 1000).toFixed(2)}s` : '—'}</strong></div>
              <span className="metric-foot">Hard termination</span>
            </article>
          </section>

          <section className="dashboard-grid">
            <article className="panel posture-panel" id="policy">
              <div className="panel-header">
                <div><span className="panel-kicker">Current workspace</span><h2>Policy posture</h2></div>
                <label className="tenant-select-wrap">
                  <span className="sr-only">Select tenant</span>
                  <select onChange={(event) => setTenantId(event.target.value)} value={tenantId}>
                    {policies.map((entry) => <option key={entry.tenantId} value={entry.tenantId}>{entry.displayName}</option>)}
                  </select>
                  <Icon name="chevron" size={15} />
                </label>
              </div>

              <div className="posture-body">
                <div className="score-wrap">
                  <div className="score-ring" style={{ '--score': policyStrength } as CSSProperties}>
                    <div className="score-inner"><strong>{policyStrength}</strong><span>/ 100</span></div>
                  </div>
                  <div className="score-caption"><span className="status-dot" /> Strong posture</div>
                </div>
                <div className="control-list">
                  {controlItems.map((item) => (
                    <div className="control-row" key={item.label}>
                      <div className="control-symbol"><Icon name={item.icon} size={17} /></div>
                      <div><strong>{item.label}</strong><span>{item.value}</span></div>
                      <span className={`control-state ${item.active ? 'enabled' : 'optional'}`}>
                        {item.active ? <Icon name="check" size={13} /> : null}{item.active ? 'Enforced' : 'Optional'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div className="policy-footer">
                <div><span>Risk profile</span><strong className={`risk-text ${policy?.riskLevel ?? 'low'}`}>{policy?.riskLevel ?? '—'}</strong></div>
                <div><span>Network</span><strong>{policy?.allowNetwork ? 'Allowlisted' : 'Isolated'}</strong></div>
                <div><span>Artifact signing</span><strong>{policy?.requireSignedPlugins ? 'Required' : 'Optional'}</strong></div>
              </div>
            </article>

            <article className="panel runtime-panel" id="runtime">
              <div className="panel-header">
                <div><span className="panel-kicker">Runtime fleet</span><h2>Isolation status</h2></div>
                <button aria-label="Runtime options" className="more-button" type="button">•••</button>
              </div>
              <div className="runtime-visual">
                <div className="orbit orbit-outer"><span /><span /><span /></div>
                <div className="orbit orbit-inner"><span /><span /></div>
                <div className="runtime-core"><Icon name="cube" size={27} /><span>WASM</span></div>
              </div>
              <div className="runtime-status"><span className="pulse-dot" /><strong>All sandboxes healthy</strong><span>Policy sync completed moments ago</span></div>
              <div className="runtime-stats">
                <div><span>Isolation</span><strong>Process + WASI</strong></div>
                <div><span>Egress</span><strong>{policy?.allowNetwork ? 'Filtered' : 'Blocked'}</strong></div>
              </div>
            </article>
          </section>

          <section className="panel validation-panel" id="validation">
            <div className="validation-intro">
              <div className="validation-icon"><Icon name="code" size={23} /></div>
              <span className="panel-kicker">Developer workspace</span>
              <h2>Compile a plugin into a sandbox-safe artifact</h2>
              <p>Write your plugin logic in the editor, compile it to a Wasm-style payload, and inspect the sandbox metrics before execution.</p>
              <div className="validation-steps">
                <div><span>01</span><p><strong>Author plugin</strong>Build a simple parser or transformation function.</p></div>
                <div><span>02</span><p><strong>Compile safely</strong>Send it to the backend compiler for sandbox-aware validation.</p></div>
                <div><span>03</span><p><strong>Inspect metrics</strong>Review execution time and memory footprint.</p></div>
              </div>
            </div>

            <div className="validation-form-wrap">
              <label className="field field-wide"><span>Plugin name</span><div className="input-shell"><Icon name="cube" size={17} /><input onChange={(event) => setPluginName(event.target.value)} placeholder="payment-guard.wasm" value={pluginName} /></div></label>
              <label className="field field-wide"><span>Plugin source</span><textarea onChange={(event) => setSourceCode(event.target.value)} placeholder="def run(data):\n    return data" style={{ minHeight: 180, resize: 'vertical', width: '100%', padding: '12px', borderRadius: 12, background: 'rgba(15, 23, 42, 0.65)', border: '1px solid rgba(148, 163, 184, 0.16)', color: 'white' }} value={sourceCode} /></label>
              <button className="run-button" disabled={isCompiling} onClick={handleCompile} type="button">
                {isCompiling ? <span className="button-spinner" /> : <Icon name="terminal" size={18} />}
                {isCompiling ? 'Compiling...' : 'Compile to Wasm'}
              </button>
              {compileResult && (
                <div className={`validation-result ${compileResult.compiled ? 'approved' : 'rejected'}`}>
                  <div className="result-icon"><Icon name={compileResult.compiled ? 'check' : 'x'} size={21} /></div>
                  <div className="result-copy">
                    <span>{compileResult.compiled ? 'Payload ready' : 'Blocked'}</span>
                    <strong>{compileResult.pluginName}</strong>
                    <p>{compileResult.message}</p>
                  </div>
                  <div className="result-score">
                    <strong>{compileResult.executionTimeMs}ms</strong>
                    <span>{compileResult.memoryBytes} bytes</span>
                  </div>
                </div>
              )}
            </div>
          </section>

          <section className="panel validation-panel" id="validation">
            <div className="validation-intro">
              <div className="validation-icon"><Icon name="terminal" size={23} /></div>
              <span className="panel-kicker">Preflight scanner</span>
              <h2>Validate a plugin artifact</h2>
              <p>Evaluate imports, memory, network behavior, signing, and execution time against the selected tenant policy.</p>
              <div className="validation-steps">
                <div><span>01</span><p><strong>Describe artifact</strong>Provide its runtime requirements.</p></div>
                <div><span>02</span><p><strong>Evaluate policy</strong>Run deterministic guard checks.</p></div>
                <div><span>03</span><p><strong>Review decision</strong>Inspect its score and violations.</p></div>
              </div>
            </div>

            <div className="validation-form-wrap">
              <div className="form-grid">
                <label className="field field-wide"><span>Plugin artifact</span><div className="input-shell"><Icon name="cube" size={17} /><input onChange={(event) => setPluginName(event.target.value)} placeholder="plugin-name.wasm" value={pluginName} /></div></label>
                <label className="field field-wide"><span>Requested imports</span><div className="input-shell"><Icon name="code" size={17} /><input onChange={(event) => setImportsText(event.target.value)} placeholder="console, env" value={importsText} /></div><small>Separate imports with commas</small></label>
                <label className="field"><span>Memory pages</span><div className="input-shell"><Icon name="memory" size={17} /><input min="0" onChange={(event) => setMemoryPages(Number(event.target.value))} type="number" value={memoryPages} /></div></label>
                <label className="field"><span>Execution time</span><div className="input-shell suffix"><Icon name="clock" size={17} /><input min="0" onChange={(event) => setExecutionTimeMs(Number(event.target.value))} type="number" value={executionTimeMs} /><em>ms</em></div></label>
                <label className="field field-wide"><span>Network host</span><div className={`input-shell ${!network ? 'disabled' : ''}`}><Icon name="globe" size={17} /><input disabled={!network} onChange={(event) => setHost(event.target.value)} placeholder={network ? 'api.example.com' : 'Enable network access first'} value={host} /></div></label>
              </div>

              <div className="toggle-row">
                <label className="toggle-field"><input checked={signed} onChange={(event) => setSigned(event.target.checked)} type="checkbox" /><span className="toggle-control" /><div><strong>Signed artifact</strong><small>Signature verified by trusted issuer</small></div></label>
                <label className="toggle-field"><input checked={network} onChange={(event) => setNetwork(event.target.checked)} type="checkbox" /><span className="toggle-control" /><div><strong>Network access</strong><small>Plugin requests outbound egress</small></div></label>
              </div>

              {validationError && <div className="form-error"><Icon name="x" size={15} />{validationError}</div>}
              <button className="run-button" disabled={isValidating} onClick={handleValidate} type="button">
                {isValidating ? <span className="button-spinner" /> : <Icon name="scan" size={18} />}
                {isValidating ? 'Evaluating policy...' : 'Run security validation'}
              </button>

              {validation && (
                <div className={`validation-result ${validation.valid ? 'approved' : 'rejected'}`}>
                  <div className="result-icon"><Icon name={validation.valid ? 'check' : 'x'} size={21} /></div>
                  <div className="result-copy">
                    <span>{validation.valid ? 'Artifact approved' : 'Artifact blocked'}</span>
                    <strong>{validation.pluginName}</strong>
                    <p>{validation.valid ? 'All policy checks passed. This plugin is cleared for execution.' : validation.violations.join(' · ')}</p>
                  </div>
                  <div className="result-score"><strong>{validation.score}</strong><span>Trust score</span></div>
                </div>
              )}
            </div>
          </section>

          <section className="panel audit-panel" id="audit">
            <div className="panel-header audit-header">
              <div><span className="panel-kicker">Security telemetry</span><h2>Recent validation activity</h2></div>
              <div className="audit-summary"><span><i className="summary-dot approved" />{auditEntries.filter((entry) => entry.valid).length} approved</span><span><i className="summary-dot rejected" />{auditEntries.filter((entry) => !entry.valid).length} blocked</span></div>
            </div>

            <div className="audit-table-wrap">
              <table className="audit-table">
                <thead><tr><th>Artifact</th><th>Decision</th><th>Policy detail</th><th>Observed</th><th><span className="sr-only">Open</span></th></tr></thead>
                <tbody>
                  {filteredAuditEntries.map((entry) => (
                    <tr key={entry.id}>
                      <td><div className="artifact-cell"><span><Icon name="cube" size={16} /></span><div><strong>{entry.pluginName}</strong><small>{entry.tenantId} workspace</small></div></div></td>
                      <td><span className={`decision-badge ${entry.valid ? 'approved' : 'rejected'}`}><Icon name={entry.valid ? 'check' : 'x'} size={13} />{entry.valid ? 'Approved' : 'Blocked'}</span></td>
                      <td><span className="policy-detail">{entry.violations[0] ?? 'All checks passed'}</span></td>
                      <td><time dateTime={entry.timestamp}>{formatRelativeTime(entry.timestamp)}</time></td>
                      <td><button aria-label={`View ${entry.pluginName}`} className="row-open" type="button"><Icon name="chevron" size={16} /></button></td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {!filteredAuditEntries.length && <div className="empty-state"><Icon name="search" size={22} /><strong>No matching events</strong><span>Try a different artifact name or decision.</span></div>}
            </div>
          </section>

          <footer className="page-footer" id="settings">
            <span><Icon name="shield" size={15} /> WasmBox Security Cloud</span>
            <span>Policy engine v0.1 · Runtime status operational</span>
          </footer>
        </div>
      </main>
    </div>
  );
}
