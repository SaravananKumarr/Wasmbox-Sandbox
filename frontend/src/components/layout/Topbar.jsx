import {
  Bell,
  ChevronDown,
  Command,
  Search,
  ShieldCheck,
} from "lucide-react";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";
import * as Avatar from "@radix-ui/react-avatar";

function Topbar() {
  return (
    <header
      className="
        flex h-20 items-center justify-between
        border-b border-slate-800/80
        bg-[#090c15]/80
        px-6
        backdrop-blur-xl
      "
    >
      {/* Left side */}
      <div>
        <h1 className="text-lg font-semibold text-slate-100">
          Developer Portal
        </h1>

        <p className="mt-0.5 text-xs text-slate-500">
          Manage and monitor your WasmBox plugins
        </p>
      </div>

      {/* Right side */}
      <div className="flex items-center gap-3">
        {/* Search */}
        <button
          type="button"
          className="
            hidden min-w-[220px] items-center gap-3
            rounded-xl border border-slate-800
            bg-slate-900/70
            px-3 py-2.5
            text-sm text-slate-500
            transition
            hover:border-slate-700
            hover:bg-slate-900
            md:flex
          "
        >
          <Search className="h-4 w-4" />

          <span className="flex-1 text-left">
            Search...
          </span>

          <span
            className="
              flex items-center gap-1
              rounded-md border border-slate-700
              bg-slate-800
              px-1.5 py-0.5
              text-[10px] text-slate-400
            "
          >
            <Command className="h-3 w-3" /> K
          </span>
        </button>

        {/* Sandbox status */}
        <div
          className="
            hidden items-center gap-2
            rounded-xl border border-emerald-500/10
            bg-emerald-500/5
            px-3 py-2
            lg:flex
          "
        >
          <ShieldCheck className="h-4 w-4 text-emerald-400" />

          <span className="text-xs font-medium text-emerald-400">
            Sandbox Online
          </span>
        </div>

        {/* Notifications */}
        <button
          type="button"
          className="
            relative flex h-10 w-10
            items-center justify-center
            rounded-xl
            border border-slate-800
            bg-slate-900/70
            text-slate-400
            transition
            hover:border-slate-700
            hover:bg-slate-800
            hover:text-white
          "
        >
          <Bell className="h-4 w-4" />

          <span
            className="
              absolute right-2 top-2
              h-1.5 w-1.5
              rounded-full bg-violet-500
              ring-2 ring-[#090c15]
            "
          />
        </button>

        {/* User menu */}
        <DropdownMenu.Root>
          <DropdownMenu.Trigger asChild>
            <button
              type="button"
              className="
                flex items-center gap-2
                rounded-xl
                border border-slate-800
                bg-slate-900/70
                p-1.5 pr-3
                transition
                hover:border-slate-700
                hover:bg-slate-800
              "
            >
              <Avatar.Root
                className="
                  flex h-8 w-8
                  items-center justify-center
                  overflow-hidden
                  rounded-lg
                  bg-gradient-to-br
                  from-violet-600
                  to-cyan-500
                "
              >
                <Avatar.Fallback
                  className="text-xs font-semibold text-white"
                >
                  MY
                </Avatar.Fallback>
              </Avatar.Root>

              <div className="hidden text-left sm:block">
                <p className="text-xs font-medium text-slate-200">
                  Developer
                </p>

                <p className="text-[10px] text-slate-500">
                  Workspace
                </p>
              </div>

              <ChevronDown className="h-3.5 w-3.5 text-slate-500" />
            </button>
          </DropdownMenu.Trigger>

          <DropdownMenu.Portal>
            <DropdownMenu.Content
              align="end"
              sideOffset={8}
              className="
                z-50 min-w-[190px]
                rounded-xl
                border border-slate-800
                bg-[#0d111c]
                p-1.5
                shadow-2xl shadow-black/40
              "
            >
              <DropdownMenu.Item
                className="
                  cursor-pointer rounded-lg
                  px-3 py-2
                  text-sm text-slate-300
                  outline-none
                  transition
                  hover:bg-slate-800
                  focus:bg-slate-800
                "
              >
                Profile
              </DropdownMenu.Item>

              <DropdownMenu.Item
                className="
                  cursor-pointer rounded-lg
                  px-3 py-2
                  text-sm text-slate-300
                  outline-none
                  transition
                  hover:bg-slate-800
                  focus:bg-slate-800
                "
              >
                Workspace settings
              </DropdownMenu.Item>

              <DropdownMenu.Separator
                className="my-1 h-px bg-slate-800"
              />

              <DropdownMenu.Item
                className="
                  cursor-pointer rounded-lg
                  px-3 py-2
                  text-sm text-red-400
                  outline-none
                  transition
                  hover:bg-red-500/10
                  focus:bg-red-500/10
                "
              >
                Sign out
              </DropdownMenu.Item>
            </DropdownMenu.Content>
          </DropdownMenu.Portal>
        </DropdownMenu.Root>
      </div>
    </header>
  );
}

export default Topbar;