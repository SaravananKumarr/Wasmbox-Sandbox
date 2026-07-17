import { describe, expect, it } from 'vitest';
import { compilePlugin } from './compilerService.js';

describe('compilePlugin', () => {
  it('compiles a safe plugin payload', () => {
    const result = compilePlugin({
      tenantId: 'alpha',
      pluginName: 'parser',
      sourceCode: 'def run(data):\n    return data',
    });

    expect(result.compiled).toBe(true);
    expect(result.executionTimeMs).toBe(3);
    expect(result.wasmBinary.length).toBeGreaterThan(0);
  });

  it('blocks plugins that attempt privileged operations', () => {
    const result = compilePlugin({
      tenantId: 'alpha',
      pluginName: 'danger',
      sourceCode: 'import os\nprint(os.listdir("/"))',
    });

    expect(result.compiled).toBe(false);
    expect(result.memoryBytes).toBe(0);
    expect(result.message).toContain('blocked');
  });
});
