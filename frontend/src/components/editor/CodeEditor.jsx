import Editor from "@monaco-editor/react";

function CodeEditor({ value, onChange, language = "python", readOnly = false }) {
  const handleEditorChange = (newValue) => {
    if (onChange) {
      onChange(newValue || "");
    }
  };

  return (
    <div className="relative h-full w-full overflow-hidden rounded-xl border border-blue-100 bg-white shadow-sm">
      <Editor
        height="100%"
        language={language}
        theme="vs-light"
        value={value}
        onChange={handleEditorChange}
        options={{
          fontSize: 13.5,
          fontFamily: "'JetBrains Mono', 'Fira Code', Consolas, monospace",
          minimap: { enabled: false },
          scrollBeyondLastLine: false,
          smoothScrolling: true,
          cursorBlinking: "smooth",
          cursorSmoothCaretAnimation: "on",
          padding: { top: 16, bottom: 16 },
          readOnly,
          renderLineHighlight: "all",
          tabSize: 4,
          automaticLayout: true,
          folding: true,
          lineNumbersMinChars: 3,
        }}
        loading={
          <div className="flex h-full items-center justify-center text-sm text-slate-500">
            Loading Monaco Editor...
          </div>
        }
      />
    </div>
  );
}

export default CodeEditor;
