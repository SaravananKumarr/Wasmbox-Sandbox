import apiRequest from "./api";

export const pluginService = {
  getPlugins() {
    return apiRequest("/plugins");
  },

  getPluginById(id) {
    return apiRequest(`/plugins/${id}`);
  },

  createPlugin(pluginData) {
    return apiRequest("/plugins", {
      method: "POST",
      body: JSON.stringify(pluginData),
    });
  },

  updatePlugin(id, updates) {
    return apiRequest(`/plugins/${id}`, {
      method: "PUT",
      body: JSON.stringify(updates),
    });
  },

  deletePlugin(id) {
    return apiRequest(`/plugins/${id}`, { method: "DELETE" });
  },
};

export default pluginService;
