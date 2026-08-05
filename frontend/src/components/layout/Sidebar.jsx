import { useState } from "react";
import { motion } from "motion/react";
import { useLocation, useNavigate } from "react-router-dom";

import {
  LayoutDashboard,
  Boxes,
  Code2,
  Activity,
  ShieldCheck,
  Settings,
  ChevronLeft,
  ChevronRight,
} from "lucide-react";

import Tooltip from "../common/Tooltip";

const navItems = [
  {
    label: "Dashboard",
    icon: LayoutDashboard,
    path: "/dashboard",
  },
  {
    label: "Plugins",
    icon: Boxes,
    path: "/plugins",
  },
  {
    label: "Editor",
    icon: Code2,
    path: "/editor",
  },
  {
    label: "Metrics",
    icon: Activity,
    path: "/metrics",
  },
  {
    label: "Security",
    icon: ShieldCheck,
    path: "/security",
  },
  {
    label: "Settings",
    icon: Settings,
    path: "/settings",
  },
];

function Sidebar() {
  const [collapsed, setCollapsed] = useState(false);

  const location = useLocation();
  const navigate = useNavigate();

  const handleNavigation = (item) => {
    if (item.path) {
      navigate(item.path);
    }
  };

  return (
    <motion.aside
      animate={{
        width: collapsed ? 84 : 240,
      }}
      transition={{
        duration: 0.22,
        ease: "easeInOut",
      }}
      className="
        relative
        flex
        min-h-screen
        flex-col
        border-r
        border-blue-100/80
        bg-slate-50
      "
    >
      {/* Logo */}
      <div
        className="
          flex
          h-20
          items-center
          border-b
          border-blue-100/80
          px-5
        "
      >
        <div
          className="
            flex
            h-10
            w-10
            shrink-0
            items-center
            justify-center
            rounded-xl
            bg-gradient-to-br
            from-sky-500
            to-blue-600
            font-bold
            text-white
            shadow-lg
            shadow-sky-200/60
          "
        >
          W
        </div>

        {!collapsed && (
          <motion.div
            initial={{
              opacity: 0,
              x: -6,
            }}
            animate={{
              opacity: 1,
              x: 0,
            }}
            className="ml-3"
          >
            <p className="font-semibold text-slate-900">
              WasmBox
            </p>

            <p className="text-xs text-slate-600">
              Developer Portal
            </p>
          </motion.div>
        )}
      </div>

      {/* Navigation */}
      <nav className="flex-1 space-y-2 px-3 py-5">
        {navItems.map((item) => {
          const Icon = item.icon;

          const isActive =
            item.path &&
            (location.pathname === item.path ||
              (item.path === "/dashboard" &&
                location.pathname === "/"));

          const button = (
            <button
              type="button"
              onClick={() => handleNavigation(item)}
              disabled={!item.path}
              className={`
                group
                relative
                flex
                w-full
                items-center
                gap-3
                rounded-xl
                px-3
                py-3
                text-sm
                transition-all
                duration-200

                ${
                  isActive
                    ? "text-slate-900"
                    : item.path
                    ? "text-slate-600 hover:bg-slate-100 hover:text-slate-900"
                    : "cursor-default text-slate-400"
                }
              `}
            >
              {isActive && (
                <motion.div
                  layoutId="sidebar-active"
                  className="
                    absolute
                    inset-0
                    rounded-xl
                    border
                    border-sky-200/80
                    bg-sky-100/70
                  "
                  transition={{
                    type: "spring",
                    stiffness: 380,
                    damping: 30,
                  }}
                />
              )}

              <Icon
                className={`
                  relative
                  z-10
                  h-5
                  w-5
                  shrink-0

                  ${
                    isActive
                      ? "text-blue-600"
                      : item.path
                      ? "text-slate-500 group-hover:text-slate-700"
                      : "text-slate-500"
                  }
                `}
              />

              {!collapsed && (
                <span className="relative z-10">
                  {item.label}

                  {!item.path && (
                    <span className="ml-2 text-[9px] uppercase tracking-wider text-slate-700">
                      Soon
                    </span>
                  )}
                </span>
              )}
            </button>
          );

          return collapsed ? (
            <Tooltip
              key={item.label}
              content={
                item.path
                  ? item.label
                  : `${item.label} — coming soon`
              }
            >
              {button}
            </Tooltip>
          ) : (
            <div key={item.label}>
              {button}
            </div>
          );
        })}
      </nav>

      {/* Sandbox status */}
      <div className="border-t border-blue-100/80 p-3">
        {!collapsed && (
          <div
            className="
              mb-3
              rounded-xl
              border
              border-blue-100/80
              bg-sky-50
              px-3
              py-3
            "
          >
            <div className="flex items-center gap-2">
              <div
                className="
                  h-2
                  w-2
                  rounded-full
                  bg-emerald-400
                  shadow-[0_0_10px_rgba(52,211,153,0.8)]
                "
              />

              <span className="text-xs font-medium text-emerald-400">
                Sandbox Online
              </span>
            </div>

            <p className="mt-1 text-xs text-slate-500">
              All systems operational
            </p>
          </div>
        )}

        {/* Collapse button */}
        <Tooltip
          content={
            collapsed
              ? "Expand sidebar"
              : "Collapse sidebar"
          }
        >
          <button
            type="button"
            onClick={() =>
              setCollapsed((value) => !value)
            }
            className="
              flex
              w-full
              items-center
              justify-center
              rounded-xl
              border
              border-blue-100
              bg-white
              py-2.5
              text-slate-700
              transition
              hover:border-sky-300
              hover:bg-slate-100
              hover:text-slate-900
            "
          >
            {collapsed ? (
              <ChevronRight className="h-4 w-4" />
            ) : (
              <ChevronLeft className="h-4 w-4" />
            )}
          </button>
        </Tooltip>
      </div>
    </motion.aside>
  );
}

export default Sidebar;