import { motion } from "motion/react";

function MetricCard({
  title,
  value,
  subtitle,
  icon: Icon,
  trend,
  trendType = "positive",
}) {
  const trendClass =
    trendType === "positive"
      ? "text-emerald-400"
      : trendType === "negative"
      ? "text-red-400"
      : "text-slate-400";

  return (
    <motion.div
      initial={{
        opacity: 0,
        y: 14,
      }}
      animate={{
        opacity: 1,
        y: 0,
      }}
      whileHover={{
        y: -4,
      }}
      transition={{
        duration: 0.25,
      }}
      className="
        rounded-2xl
        border border-slate-800/80
        bg-[#0d111c]/90
        p-5
        shadow-xl shadow-black/10
      "
    >
      <div className="flex items-start justify-between gap-4">
        <div>
          <p className="text-sm font-medium text-slate-400">
            {title}
          </p>

          <h3 className="mt-3 text-3xl font-bold tracking-tight text-slate-100">
            {value}
          </h3>
        </div>

        {Icon && (
          <div
            className="
              flex h-11 w-11
              items-center justify-center
              rounded-xl
              border border-violet-500/20
              bg-violet-500/10
              text-violet-400
            "
          >
            <Icon className="h-5 w-5" />
          </div>
        )}
      </div>

      <div className="mt-4 flex items-center gap-2">
        {trend && (
          <span className={`text-xs font-medium ${trendClass}`}>
            {trend}
          </span>
        )}

        {subtitle && (
          <span className="text-xs text-slate-500">
            {subtitle}
          </span>
        )}
      </div>
    </motion.div>
  );
}

export default MetricCard;