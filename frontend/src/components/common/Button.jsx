import { LoaderCircle } from "lucide-react";

const variants = {
  primary:
    "bg-violet-600 text-white hover:bg-violet-500 shadow-lg shadow-violet-950/30",

  secondary:
    "border border-slate-700 bg-slate-900 text-slate-200 hover:bg-slate-800",

  ghost:
    "bg-transparent text-slate-400 hover:bg-slate-800 hover:text-white",

  danger:
    "bg-red-600 text-white hover:bg-red-500",
};

const sizes = {
  sm: "h-8 px-3 text-xs",
  md: "h-10 px-4 text-sm",
  lg: "h-12 px-6 text-base",
};

function Button({
  children,
  variant = "primary",
  size = "md",
  icon: Icon,
  loading = false,
  disabled = false,
  className = "",
  type = "button",
  ...props
}) {
  return (
    <button
      type={type}
      disabled={disabled || loading}
      className={`
        inline-flex items-center justify-center gap-2
        rounded-xl font-medium
        transition-all duration-200
        active:scale-[0.97]
        focus-visible:outline-none
        focus-visible:ring-2
        focus-visible:ring-violet-500
        disabled:pointer-events-none
        disabled:opacity-50
        ${variants[variant]}
        ${sizes[size]}
        ${className}
      `}
      {...props}
    >
      {loading ? (
        <LoaderCircle className="h-4 w-4 animate-spin" />
      ) : Icon ? (
        <Icon className="h-4 w-4" />
      ) : null}

      {children}
    </button>
  );
}

export default Button;