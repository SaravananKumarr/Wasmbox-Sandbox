import { useState } from "react";
import { User, Mail, Lock } from "lucide-react";
import Button from "../components/common/Button";

function Register() {
  const [username, setUsername] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    setLoading(true);

    try {
      const res = await fetch("/api/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, email, password }),
      });

      if (!res.ok) {
        const data = await res.json().catch(() => ({}));
        throw new Error(data.detail || "Registration failed");
      }

      setSuccess("Account created. You can now sign in.");
    } catch (err) {
      setError(err.message || "Unexpected error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-white">
      <div className="w-full max-w-md">
        <div className="rounded-2xl border border-blue-100 bg-white p-8 shadow-sm">
          <h2 className="text-2xl font-bold text-slate-900">Create your account</h2>
          <p className="mt-2 text-sm text-slate-500">Start building plugins and monitoring executions.</p>

          <form className="mt-6 space-y-4" onSubmit={handleSubmit}>
            <label className="block">
              <span className="text-xs text-slate-600">Username</span>
              <div className="mt-1 flex items-center gap-2 rounded-lg border border-blue-100 bg-slate-50 px-3 py-2">
                <User className="h-4 w-4 text-slate-500" />
                <input
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  type="text"
                  required
                  className="w-full bg-transparent outline-none text-slate-900"
                  placeholder="your-username"
                />
              </div>
            </label>

            <label className="block">
              <span className="text-xs text-slate-600">Email</span>
              <div className="mt-1 flex items-center gap-2 rounded-lg border border-blue-100 bg-slate-50 px-3 py-2">
                <Mail className="h-4 w-4 text-slate-500" />
                <input
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  type="email"
                  required
                  className="w-full bg-transparent outline-none text-slate-900"
                  placeholder="you@company.com"
                />
              </div>
            </label>

            <label className="block">
              <span className="text-xs text-slate-600">Password</span>
              <div className="mt-1 flex items-center gap-2 rounded-lg border border-blue-100 bg-slate-50 px-3 py-2">
                <Lock className="h-4 w-4 text-slate-500" />
                <input
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  type="password"
                  required
                  className="w-full bg-transparent outline-none text-slate-900"
                  placeholder="Strong password"
                />
              </div>
            </label>

            {error && <p className="text-sm text-red-600">{error}</p>}
            {success && <p className="text-sm text-emerald-600">{success}</p>}

            <div className="pt-2">
              <Button type="submit" variant="primary" loading={loading} className="w-full">
                Create account
              </Button>
            </div>

            <p className="mt-4 text-center text-sm text-slate-500">
              Already have an account? <a href="/login" className="text-sky-600 hover:underline">Sign in</a>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Register;
