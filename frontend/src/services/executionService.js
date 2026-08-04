import apiRequest from "./api";

export const executionService = {
  executePlugin(pluginId, code, inputPayload = "{}") {
    return apiRequest("/execute", {
      method: "POST",
      body: JSON.stringify({ plugin_id: pluginId, code, input: inputPayload }),
    });
  },

  getExecutionHistory() {
    return apiRequest("/executions/history");
  },

  getMetricsSummary() {
    return apiRequest("/metrics/summary");
  },
};

export default executionService;
