import apiRequest from "./api";

const executionService = {
  executePlugin(code, input) {
    return apiRequest("/run", { method: "POST", body: JSON.stringify({ code, input }) });
  },
};

export default executionService;
