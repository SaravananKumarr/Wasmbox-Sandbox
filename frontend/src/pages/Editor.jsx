import { useEffect, useState } from "react";
import usePluginStore from "../stores/pluginStore";
import useExecutionStore from "../stores/executionStore";

import EditorToolbar from "../components/editor/EditorToolbar";
import CodeEditor from "../components/editor/CodeEditor";
import ExecutionResult from "../components/editor/ExecutionResult";
import Console from "../components/editor/Console";

function Editor() {
  const {
    plugins,
    activePlugin,
    activeCode,
    fetchPlugins,
    setActiveCode,
    saveCurrentCode,
    loading: pluginLoading,
  } = usePluginStore();

  const {
    status: executionStatus,
    executionResult,
    logs,
    inputPayload,
    setInputPayload,
    clearLogs,
    runExecution,
  } = useExecutionStore();

  const [language, setLanguage] = useState("python");

  useEffect(() => {
    fetchPlugins();
  }, [fetchPlugins]);

  const handleSave = () => {
    saveCurrentCode();
  };

  const handleRun = () => {
    runExecution(activePlugin?.id, activeCode, language);
  };

  return (
    <div className="flex flex-col gap-5">
      {/* Top Toolbar */}
      <EditorToolbar
        pluginName={activePlugin?.name || "customer_formatter.py"}
        language={language}
        onLanguageChange={setLanguage}
        onSave={handleSave}
        onRun={handleRun}
        saving={pluginLoading}
        executionStatus={executionStatus}
      />

      {/* Main Grid Section */}
      <div className="grid gap-5 xl:grid-cols-[1.6fr_1fr]" style={{ minHeight: "440px" }}>
        {/* Code Editor Container */}
        <div className="h-[440px]">
          <CodeEditor
            value={activeCode}
            onChange={setActiveCode}
            language={language}
          />
        </div>

        {/* Input & Execution Metrics Panel */}
        <div className="h-[440px]">
          <ExecutionResult
            result={executionResult}
            status={executionStatus}
            inputPayload={inputPayload}
            onInputPayloadChange={setInputPayload}
          />
        </div>
      </div>

      {/* Bottom Terminal / Console Log Area */}
      <div className="h-[240px]">
        <Console
          logs={logs}
          onClear={clearLogs}
          status={executionStatus}
        />
      </div>
    </div>
  );
}

export default Editor;
