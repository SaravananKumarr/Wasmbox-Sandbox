import { create } from "zustand";
import pluginService from "../services/pluginService";

export const usePluginStore = create((set, get) => ({
  plugins: [],
  activePlugin: null,
  activeCode: "",
  searchQuery: "",
  loading: false,
  error: null,

  fetchPlugins: async () => {
    set({ loading: true, error: null });
    try {
      const plugins = await pluginService.getPlugins();
      set({ plugins, loading: false });
      if (!get().activePlugin && plugins.length > 0) {
        get().selectPlugin(plugins[0]);
      }
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },

  selectPlugin: (plugin) => {
    set({
      activePlugin: plugin,
      activeCode: plugin ? plugin.code || "" : "",
    });
  },

  setActiveCode: (code) => {
    set({ activeCode: code });
  },

  setSearchQuery: (query) => {
    set({ searchQuery: query });
  },

  saveCurrentCode: async () => {
    const { activePlugin, activeCode } = get();
    if (!activePlugin) return;

    set({ loading: true });
    try {
      const updated = await pluginService.updatePlugin(activePlugin.id, {
        code: activeCode,
      });
      
      set((state) => ({
        plugins: state.plugins.map((p) =>
          p.id === activePlugin.id ? { ...p, ...updated, code: activeCode } : p
        ),
        activePlugin: { ...activePlugin, ...updated, code: activeCode },
        loading: false,
      }));
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },

  createNewPlugin: async (name, description) => {
    set({ loading: true });
    try {
      const newPlugin = await pluginService.createPlugin({ name, description });
      set((state) => ({
        plugins: [newPlugin, ...state.plugins],
        activePlugin: newPlugin,
        activeCode: newPlugin.code,
        loading: false,
      }));
      return newPlugin;
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  },

  deletePlugin: async (pluginId) => {
    set({ loading: true, error: null });
    try {
      await pluginService.deletePlugin(pluginId);
      set((state) => {
        const plugins = state.plugins.filter((plugin) => plugin.id !== pluginId);
        const activePlugin = state.activePlugin?.id === pluginId ? plugins[0] || null : state.activePlugin;
        return { plugins, activePlugin, activeCode: activePlugin?.code || "", loading: false };
      });
    } catch (err) {
      set({ error: err.message, loading: false });
    }
  }
}));

export default usePluginStore;
