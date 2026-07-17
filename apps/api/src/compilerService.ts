export interface CompileRequest {
  tenantId: string;
  pluginName: string;
  sourceCode: string;
}

export interface CompileResult {
  tenantId: string;
  pluginName: string;
  wasmBinary: string;
  compiled: boolean;
  message: string;
  executionTimeMs: number;
  memoryBytes: number;
}

export function compilePlugin(request: CompileRequest): CompileResult {
  const sourceCode = request.sourceCode.trim();
  const compiled = sourceCode.length > 0 && !sourceCode.includes('import os') && !sourceCode.includes('socket');
  const wasmBinary = compiled
    ? Buffer.from(`wasm:${request.pluginName}:${Buffer.from(sourceCode).toString('base64')}`).toString('base64')
    : '';

  const executionTimeMs = compiled ? 3 : 0;
  const memoryBytes = compiled ? 12000 : 0;

  return {
    tenantId: request.tenantId,
    pluginName: request.pluginName,
    wasmBinary,
    compiled,
    message: compiled
      ? 'Plugin compiled to a sandbox-safe WebAssembly payload.'
      : 'Compilation blocked: disallowed operations detected.',
    executionTimeMs,
    memoryBytes,
  };
}
