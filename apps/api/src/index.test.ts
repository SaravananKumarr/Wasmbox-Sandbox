import { describe, expect, it } from 'vitest';
import { evaluatePlugin } from './policyEngine.js';

describe('tenant validation', () => {
  it('rejects unsigned plugins for strict tenants', () => {
    const result = evaluatePlugin('alpha', {
      pluginName: 'strict-plugin',
      imports: ['console', 'env'],
      memoryPages: 16,
      network: false,
      signed: false,
      executionTimeMs: 1000,
      host: '',
    });

    expect(result.valid).toBe(false);
    expect(result.violations).toContain('Plugin must be signed');
  });

  it('allows safe plugins for a tenant with a permissive policy', () => {
    const result = evaluatePlugin('gamma', {
      pluginName: 'safe-plugin',
      imports: ['console', 'env'],
      memoryPages: 24,
      network: true,
      signed: false,
      executionTimeMs: 1200,
      host: 'localhost',
    });

    expect(result.valid).toBe(true);
    expect(result.violations).toEqual([]);
  });
});
