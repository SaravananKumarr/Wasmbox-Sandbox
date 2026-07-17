export interface TenantPolicy {
  tenantId: string;
  displayName: string;
  allowedImports: string[];
  maxMemoryPages: number;
  allowNetwork: boolean;
  requireSignedPlugins: boolean;
  maxExecutionTimeMs: number;
  allowedHosts: string[];
  riskLevel: 'low' | 'medium' | 'high';
}

export interface PluginEvaluationRequest {
  pluginName: string;
  imports?: string[];
  memoryPages?: number;
  network?: boolean;
  signed?: boolean;
  executionTimeMs?: number;
  host?: string;
}

export interface ValidationResult {
  pluginName: string;
  tenantId: string;
  valid: boolean;
  violations: string[];
  score: number;
  riskLevel: 'low' | 'medium' | 'high';
}

export interface AuditEntry {
  id: string;
  tenantId: string;
  pluginName: string;
  timestamp: string;
  valid: boolean;
  violations: string[];
}

export const tenantPolicies: TenantPolicy[] = [
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

const auditLog: AuditEntry[] = [];

export function getTenantPolicies(): TenantPolicy[] {
  return tenantPolicies;
}

export function getTenantPolicy(tenantId: string): TenantPolicy | undefined {
  return tenantPolicies.find((policy) => policy.tenantId === tenantId);
}

export function evaluatePlugin(tenantId: string, request: PluginEvaluationRequest): ValidationResult {
  const policy = getTenantPolicy(tenantId);
  if (!policy) {
    throw new Error(`Tenant policy not found: ${tenantId}`);
  }

  const violations: string[] = [];
  const imports = request.imports ?? [];
  const memoryPages = request.memoryPages ?? 0;
  const network = request.network ?? false;
  const signed = request.signed ?? false;
  const executionTimeMs = request.executionTimeMs ?? 0;
  const host = request.host ?? '';

  if (policy.requireSignedPlugins && !signed) {
    violations.push('Plugin must be signed');
  }

  const disallowedImports = imports.filter((entry) => !policy.allowedImports.includes(entry));
  if (disallowedImports.length > 0) {
    violations.push(`Disallowed imports: ${disallowedImports.join(', ')}`);
  }

  if (memoryPages > policy.maxMemoryPages) {
    violations.push(`Memory exceeds limit (${policy.maxMemoryPages} pages)`);
  }

  if (!policy.allowNetwork && network) {
    violations.push('Network access is not allowed for this tenant');
  }

  if (executionTimeMs > policy.maxExecutionTimeMs) {
    violations.push(`Execution time exceeds limit (${policy.maxExecutionTimeMs} ms)`);
  }

  if (network && host && !policy.allowedHosts.includes(host) && policy.allowedHosts.length > 0) {
    violations.push(`Host is not in the allowlist: ${host}`);
  }

  const valid = violations.length === 0;
  const score = Math.max(0, 100 - violations.length * 20);

  return {
    pluginName: request.pluginName,
    tenantId,
    valid,
    violations,
    score,
    riskLevel: policy.riskLevel,
  };
}

export function appendAuditEntry(entry: AuditEntry): void {
  auditLog.push(entry);
  while (auditLog.length > 25) {
    auditLog.shift();
  }
}

export function getAuditEntries(tenantId?: string): AuditEntry[] {
  if (!tenantId) {
    return [...auditLog].reverse();
  }

  return auditLog.filter((entry) => entry.tenantId === tenantId).reverse();
}

export function createAuditEntry(tenantId: string, result: ValidationResult): AuditEntry {
  const entry: AuditEntry = {
    id: `${tenantId}-${Date.now()}`,
    tenantId,
    pluginName: result.pluginName,
    timestamp: new Date().toISOString(),
    valid: result.valid,
    violations: result.violations,
  };
  appendAuditEntry(entry);
  return entry;
}
