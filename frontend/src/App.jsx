function App() {
  return (
    <main className="flex min-h-screen items-center justify-center bg-[#070912] text-white">
      <section className="text-center">
        <h1 className="text-5xl font-bold tracking-tight">
          WasmBox
        </h1>

        <p className="mt-4 text-lg text-slate-400">
          Secure Multi-Tenant Python Plugin Sandbox
        </p>

        <button
          type="button"
          className="mt-8 rounded-xl bg-violet-600 px-6 py-3 font-medium transition hover:bg-violet-500"
        >
          Open Developer Portal
        </button>
      </section>
    </main>
  );
}

export default App;