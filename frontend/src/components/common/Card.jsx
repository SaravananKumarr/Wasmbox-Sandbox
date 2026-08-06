function Card({ children, className = "" }) {
  return (
    <div
      className={`rounded-2xl border border-blue-100/90 bg-white shadow-sm shadow-slate-200 ${className}`}
    >
      {children}
    </div>
  );
}

function CardHeader({ children, className = "" }) {
  return (
    <div
      className={`border-b border-blue-100/80 px-5 py-4 ${className}`}
    >
      {children}
    </div>
  );
}

function CardContent({ children, className = "" }) {
  return <div className={`p-5 ${className}`}>{children}</div>;
}

export { Card, CardHeader, CardContent };