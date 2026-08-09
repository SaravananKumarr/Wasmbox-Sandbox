import apiRequest from "./api";

const executionService = {
  async executePlugin(code, input) {
    const result = await apiRequest("/run", {
      method: "POST",
      body: JSON.stringify({ code, input }),
    });

    return {
      ...result,
      returnCode: result.return_code,
      duration: result.duration_ms,
      memory: result.memory_mb,
    };
  },
};

export default executionService;
