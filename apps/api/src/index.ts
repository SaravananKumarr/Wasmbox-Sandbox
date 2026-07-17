import express from 'express';
import cors from 'cors';
import {
  createAuditEntry,
  evaluatePlugin,
  getAuditEntries,
  getTenantPolicies,
  getTenantPolicy,
  type PluginEvaluationRequest,
} from './policyEngine.js';
import { compilePlugin, type CompileRequest } from './compilerService.js';

const app = express();
const port = Number(process.env.PORT || 4000);

app.use(cors());
app.use(express.json());

app.get('/health', (_req, res) => {
  res.json({
    status: 'ok',
    service: 'wasmbox-api',
    features: ['policy-engine', 'audit-log', 'tenant-validation'],
  });
});

app.get('/tenants', (_req, res) => {
  res.json(getTenantPolicies());
});

app.get('/tenants/:tenantId/policy', (req, res) => {
  const policy = getTenantPolicy(req.params.tenantId);
  if (!policy) {
    res.status(404).json({ error: 'Tenant policy not found' });
    return;
  }
  res.json(policy);
});

app.post('/tenants/:tenantId/validate', (req, res) => {
  const policy = getTenantPolicy(req.params.tenantId);
  if (!policy) {
    res.status(404).json({ error: 'Tenant policy not found' });
    return;
  }

  const payload = req.body as PluginEvaluationRequest;
  const result = evaluatePlugin(req.params.tenantId, payload);
  createAuditEntry(req.params.tenantId, result);

  res.json(result);
});

app.post('/plugins/compile', (req, res) => {
  const payload = req.body as CompileRequest;
  const result = compilePlugin(payload);
  res.json(result);
});

app.get('/tenants/:tenantId/audit', (req, res) => {
  res.json(getAuditEntries(req.params.tenantId));
});

app.listen(port, () => {
  console.log(`WasmBox API listening on port ${port}`);
});
