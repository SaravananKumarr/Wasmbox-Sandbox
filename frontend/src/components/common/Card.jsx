function Card({ children, className = "" }) {
  return (
    <div
      className={`rounded-2xl border border-slate-800/80
      bg-[#0d111c]/90 shadow-xl shadow-black/10 ${className}`}
    >
      {children}
    </div>
  );
}

function CardHeader({ children, className = "" }) {
  return (
    <div
      className={`border-b border-slate-800/80 px-5 py-4 ${className}`}
    >
      {children}
    </div>
  );
}

function CardContent({ children, className = "" }) {
  return <div className={`p-5 ${className}`}>{children}</div>;
}

export { Card, CardHeader, CardContent };