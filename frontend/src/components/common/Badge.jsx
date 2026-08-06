const variants = {
  default: "border-blue-100 bg-slate-50 text-slate-700",
  primary: "border-violet-500/20 bg-violet-500/10 text-violet-600",
  success: "border-emerald-500/20 bg-emerald-500/10 text-emerald-400",
  warning: "border-amber-500/20 bg-amber-500/10 text-amber-400",
  danger: "border-red-500/20 bg-red-500/10 text-red-400",
};

function Badge({ children, variant = "default", className = "" }) {
  return (
    <span
      className={`inline-flex items-center rounded-full border px-2.5 py-1
      text-xs font-medium ${variants[variant]} ${className}`}
    >
      {children}
    </span>
  );
}

export default Badge;