function App() {
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        background: "#020617",
        color: "white",
      }}
    >
      <div style={{ textAlign: "center" }}>
        <h1
          style={{
            fontSize: "60px",
            marginBottom: "20px",
          }}
        >
          WasmBox
        </h1>

        <p
          style={{
            color: "#94a3b8",
            fontSize: "22px",
          }}
        >
          Secure Multi-Tenant Plugin Sandbox
        </p>
      </div>
    </div>
  );
}

export default App;