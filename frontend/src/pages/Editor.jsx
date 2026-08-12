import { useState } from "react";

import Console from "../components/editor/Console";
import CodeEditor from "../components/editor/CodeEditor";
import EditorToolbar from "../components/editor/EditorToolbar";
import ExecutionResult from "../components/editor/ExecutionResult";
import executionService from "../services/executionService";

const starterCode = "# Write your Python plugin\nprint('Hello from WasmBox!')\n";

function Editor() {
  const [code, setCode] = useState(starterCode);
  const [inputPayload, setInputPayload] = useState('{\n  "event": "test_run"\n}');
  const [status, setStatus] = useState("idle");
  const [result, setResult] = useState(null);
  const [logs, setLogs] = useState(["[INFO] WasmBox console ready."]);

  const run = async () => {
    setStatus("running");
    setResult(null);
    setLogs(["[INFO] Sending source to /api/run..."]);
    try {
      const nextResult = await executionService.executePlugin(code, inputPayload);
      setResult(nextResult);
      setStatus(nextResult.status === "Success" ? "success" : "failed");
      setLogs((current) => [...current, ...nextResult.logs]);
    } catch (error) {
      setStatus("failed");
      setResult({
        duration: null,
        memory: null,
        returnCode: null,
        output: error.message,
        error_message: "The backend could not be reached. Start the WasmBox backend and try again.",
      });
      setLogs((current) => [...current, `[ERROR] ${error.message}`]);
    }
  };

  return (
    <div className="flex flex-col gap-5">
      <EditorToolbar onRun={run} executionStatus={status} />
      <div className="grid gap-5 xl:grid-cols-[1.6fr_1fr]" style={{ minHeight: "440px" }}>
        <div className="h-[440px]"><CodeEditor value={code} onChange={setCode} /></div>
        <div className="h-[440px]"><ExecutionResult result={result} status={status} inputPayload={inputPayload} onInputPayloadChange={setInputPayload} /></div>
      </div>
      <div className="h-[240px]"><Console logs={logs} onClear={() => setLogs([])} status={status} /></div>
    </div>
  );
}

export default Editor;
