import apiRequest from "./api";

const MOCK_PLUGINS = [
  {
    id: "1",
    name: "customer_formatter.py",
    description: "Formats and normalizes customer data before DB insertion.",
    status: "Active",
    executions: 247,
    runtime: "18 ms",
    updated: "2 min ago",
    language: "python",
    code: `def transform(payload):\n    """Format customer names and standardise email format."""\n    first_name = payload.get("first_name", "").strip().capitalize()\n    last_name = payload.get("last_name", "").strip().capitalize()\n    email = payload.get("email", "").strip().lower()\n    \n    return {\n        "status": "success",\n        "full_name": f"{first_name} {last_name}",\n        "email": email,\n        "validated": True\n    }\n\n# Main entry point\nresult = transform({\n    "first_name": "  john ",\n    "last_name": "doe  ",\n    "email": "JOHN.DOE@EXAMPLE.COM"\n})\nprint(result)`
  },
  {
    id: "2",
    name: "data_validator.py",
    description: "Validates incoming JSON payloads against business rules.",
    status: "Active",
    executions: 184,
    runtime: "24 ms",
    updated: "8 min ago",
    language: "python",
    code: `def validate(data):\n    required = ["id", "amount", "currency"]\n    missing = [field for field in required if field not in data]\n    \n    if missing:\n        return {"valid": False, "errors": f"Missing fields: {missing}"}\n    \n    if data["amount"] <= 0:\n        return {"valid": False, "errors": "Amount must be strictly positive"}\n        \n    return {"valid": True, "checksum": hash(str(data))}\n\nprint(validate({"id": "tx_9921", "amount": 149.99, "currency": "USD"}))`
  },
  {
    id: "3",
    name: "webhook_transform.py",
    description: "Transforms third-party webhook payloads into standard internal schema.",
    status: "Draft",
    executions: 0,
    runtime: "--",
    updated: "21 min ago",
    language: "python",
    code: `def process_webhook(event, body):\n    print(f"Processing webhook event: {event}")\n    return {\n        "processed_at": "2026-08-03T18:15:00Z",\n        "event_type": event,\n        "status": "ACCEPTED"\n    }\n\nprint(process_webhook("user.created", {"user_id": 4042}))`
  },
  {
    id: "4",
    name: "inventory_mapper.py",
    description: "Maps external SKU codes to internal warehouse catalog IDs.",
    status: "Active",
    executions: 96,
    runtime: "31 ms",
    updated: "1 hour ago",
    language: "python",
    code: `def map_sku(vendor_sku):\n    catalog_map = {\n        "EXT-WASM-01": "INT-WASM-A100",\n        "EXT-WASM-02": "INT-WASM-B200"\n    }\n    return catalog_map.get(vendor_sku, "UNKNOWN_SKU")\n\nprint({"internal_id": map_sku("EXT-WASM-01")})`
  }
];

export const pluginService = {
  async getPlugins() {
    try {
      return await apiRequest("/plugins");
    } catch {
      return MOCK_PLUGINS;
    }
  },

  async getPluginById(id) {
    try {
      return await apiRequest(`/plugins/${id}`);
    } catch {
      return MOCK_PLUGINS.find((p) => p.id === String(id)) || MOCK_PLUGINS[0];
    }
  },

  async createPlugin(pluginData) {
    try {
      return await apiRequest("/plugins", {
        method: "POST",
        body: JSON.stringify(pluginData),
      });
    } catch {
      const newPlugin = {
        id: String(Date.now()),
        name: pluginData.name || "untitled_plugin.py",
        description: pluginData.description || "Custom WebAssembly Python plugin.",
        status: "Draft",
        executions: 0,
        runtime: "--",
        updated: "Just now",
        language: "python",
        code: pluginData.code || "# Write your WasmBox plugin code here\nprint('Hello from WasmBox!')",
      };
      return newPlugin;
    }
  },

  async updatePlugin(id, updates) {
    try {
      return await apiRequest(`/plugins/${id}`, {
        method: "PUT",
        body: JSON.stringify(updates),
      });
    } catch {
      return { id, ...updates, updated: "Just now" };
    }
  },

  async deletePlugin(id) {
    try {
      return await apiRequest(`/plugins/${id}`, {
        method: "DELETE",
      });
    } catch {
      return { success: true, id };
    }
  }
};

export default pluginService;
