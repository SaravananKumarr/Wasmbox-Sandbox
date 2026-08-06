import { Navigate, Route, Routes } from "react-router-dom";
import Sidebar from "./components/layout/Sidebar";
import Topbar from "./components/layout/Topbar";
import Editor from "./pages/Editor";

function App() {
  return (
    <div className="flex min-h-screen bg-slate-50 text-slate-900">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <Topbar />
        <main className="flex-1 overflow-x-hidden p-6">
          <Routes>
            <Route path="/editor" element={<Editor />} />
            <Route path="*" element={<Navigate to="/editor" replace />} />
          </Routes>
        </main>
      </div>
    </div>
  );
}

export default App;
