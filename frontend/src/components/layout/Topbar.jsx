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
        border-b border-blue-100/80
        bg-white/80
        px-6
        backdrop-blur-xl
      "
    >
      {/* Left side */}
      <div>
        <h1 className="text-lg font-semibold text-slate-900">
          Developer Portal
        </h1>

        <p className="mt-0.5 text-xs text-slate-600">
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
            rounded-xl border border-blue-100
            bg-slate-50
            px-3 py-2.5
            text-sm text-slate-600
            transition
            hover:border-sky-200
            hover:bg-white
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
              rounded-md border border-blue-100
              bg-slate-100
              px-1.5 py-0.5
              text-[10px] text-slate-600
            "
          >
            <Command className="h-3 w-3 text-sky-600" /> K
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
            border border-blue-100
            bg-white
            text-slate-600
            transition
            hover:border-sky-200
            hover:bg-slate-50
            hover:text-slate-900
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
                border border-blue-100
                bg-slate-50
                p-1.5 pr-3
                transition
                hover:border-sky-200
                hover:bg-white
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
                <p className="text-xs font-medium text-slate-900">
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
                  border border-blue-100
                  bg-white
                  p-1.5
                  shadow-2xl shadow-slate-200/80
                "
              >
                <DropdownMenu.Item
                  className="
                    cursor-pointer rounded-lg
                    px-3 py-2
                    text-sm text-slate-700
                    outline-none
                    transition
                    hover:bg-slate-100
                    focus:bg-slate-100
                  "
                >
                  Profile
                </DropdownMenu.Item>

                <DropdownMenu.Item
                  className="
                    cursor-pointer rounded-lg
                    px-3 py-2
                    text-sm text-slate-700
                    outline-none
                    transition
                    hover:bg-slate-100
                    focus:bg-slate-100
                  "
                >
                  Workspace settings
                </DropdownMenu.Item>

                <DropdownMenu.Separator
                  className="my-1 h-px bg-slate-100"
                />

                <DropdownMenu.Item
                  className="
                    cursor-pointer rounded-lg
                    px-3 py-2
                    text-sm text-red-500
                    outline-none
                    transition
                    hover:bg-red-50
                    focus:bg-red-50
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