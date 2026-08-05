import { create } from "zustand";
import executionService from "../services/executionService";

export const useExecutionStore = create((set, get) => ({
  status: "idle", // 'idle' | 'running' | 'success' | 'failed'
  executionResult: null, // { duration, memory, returnCode, output }
  logs: [
    "[INFO] WasmBox Sandbox Console initialized.",
    "[INFO] Ready for WebAssembly plugin execution."
  ],
  inputPayload: `{\n  "event": "test_run",\n  "data": {\n    "first_name": "john",\n    "last_name": "doe",\n    "email": "JOHN.DOE@EXAMPLE.COM"\n  }\n}`,
  history: [],
  loadingHistory: false,

  setInputPayload: (payload) => set({ inputPayload: payload }),

  clearLogs: () => set({
    logs: ["[INFO] Console log buffer cleared."]
  }),

  runExecution: async (pluginId, code) => {
    set({
      status: "running",
      executionResult: null,
      logs: [
        `[INFO] [${new Date().toLocaleTimeString()}] Triggering WASM execution for plugin #${pluginId || "draft"}...`,
        "[INFO] Validating security sandboxing boundaries and Wasmtime memory limits..."
      ]
    });

    try {
      const result = await executionService.executePlugin(pluginId, code, get().inputPayload);
      
      const newStatus = result.status === "Success" ? "success" : "failed";

      set((state) => ({
        status: newStatus,
        executionResult: result,
        logs: [...state.logs, ...(result.logs || []), `[STATUS] Execution finished with state: ${newStatus.toUpperCase()}`],
        history: [result, ...state.history]
      }));
    } catch (err) {
      set((state) => ({
        status: "failed",
        executionResult: {
          duration: 0,
          memory: 0,
          returnCode: 1,
          output: err.message
        },
        logs: [
          ...state.logs,
          `[ERROR] Execution Exception: ${err.message}`,
          "[FATAL] Sandbox execution failed."
        ]
      }));
    }
  },

  fetchHistory: async () => {
    set({ loadingHistory: true });
    try {
      const history = await executionService.getExecutionHistory();
      set({ history, loadingHistory: false });
    } catch {
      set({ loadingHistory: false });
    }
  }
}));

export default useExecutionStore;
