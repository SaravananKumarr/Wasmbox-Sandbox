import { motion } from "motion/react";
import { useNavigate } from "react-router-dom";
import {
  MoreVertical,
  Play,
  Plus,
  Search,
  SlidersHorizontal,
} from "lucide-react";
import * as DropdownMenu from "@radix-ui/react-dropdown-menu";

import Button from "../components/common/Button";
import Badge from "../components/common/Badge";
import {
  Card,
  CardContent,
  CardHeader,
} from "../components/common/Card";
import usePluginStore from "../stores/pluginStore";

const plugins = [
  {
    id: 1,
    name: "customer_formatter.py",
    description: "Formats and normalizes customer data.",
    status: "Active",
    executions: 247,
    runtime: "18 ms",
    updated: "2 min ago",
  },
  {
    id: 2,
    name: "data_validator.py",
    description: "Validates incoming payloads before processing.",
    status: "Active",
    executions: 184,
    runtime: "24 ms",
    updated: "8 min ago",
  },
  {
    id: 3,
    name: "webhook_transform.py",
    description: "Transforms webhook payloads into a standard format.",
    status: "Draft",
    executions: 0,
    runtime: "--",
    updated: "21 min ago",
  },
  {
    id: 4,
    name: "inventory_mapper.py",
    description: "Maps external inventory fields to internal schema.",
    status: "Active",
    executions: 96,
    runtime: "31 ms",
    updated: "1 hour ago",
  },
];

function Plugins() {
  const navigate = useNavigate();
  const { selectPlugin } = usePluginStore();

  const handleOpenPlugin = (plugin) => {
    selectPlugin(plugin);
    navigate("/editor");
  };
  return (
    <div className="space-y-8">
      {/* Header */}
      <section className="flex flex-col gap-5 lg:flex-row lg:items-end lg:justify-between">
        <div>
          <p className="text-sm text-slate-500">
            Workspace
          </p>

          <h2 className="mt-1 text-3xl font-bold tracking-tight text-slate-900">
            Plugins
          </h2>

          <p className="mt-2 text-slate-400">
            Create and manage Python plugins running inside WasmBox.
          </p>
        </div>

        <Button icon={Plus} onClick={() => navigate("/editor")}>
          New Plugin
        </Button>
      </section>

      {/* Search + Filter */}
      <section className="flex flex-col gap-3 sm:flex-row">
        <div
          className="
            flex flex-1 items-center gap-3
            rounded-xl border border-blue-100
            bg-white
            px-4
            shadow-sm shadow-slate-100
          "
        >
          <Search className="h-4 w-4 text-slate-500" />

          <input
            type="text"
            placeholder="Search plugins..."
            className="
              w-full bg-transparent py-3
              text-sm text-slate-900
              outline-none
              placeholder:text-slate-500
            "
          />
        </div>

        <Button
          variant="secondary"
          icon={SlidersHorizontal}
        >
          Filter
        </Button>
      </section>

      {/* Plugin cards */}
      <section className="grid gap-5 md:grid-cols-2 xl:grid-cols-3">
        {plugins.map((plugin, index) => (
          <motion.div
            key={plugin.id}
            initial={{
              opacity: 0,
              y: 18,
            }}
            animate={{
              opacity: 1,
              y: 0,
            }}
            transition={{
              duration: 0.25,
              delay: index * 0.05,
            }}
          >
            <Card
              className="
                group h-full
                transition-all duration-200
                hover:-translate-y-1
                hover:border-violet-500/30
                hover:shadow-2xl
                hover:shadow-violet-950/20
              "
            >
              <CardHeader>
                <div className="flex items-start justify-between gap-4">
                  <div>
                    <p className="font-semibold text-slate-100">
                      {plugin.name}
                    </p>

                    <div className="mt-2">
                      <Badge
                        variant={
                          plugin.status === "Active"
                            ? "success"
                            : "warning"
                        }
                      >
                        {plugin.status}
                      </Badge>
                    </div>
                  </div>

                  <DropdownMenu.Root>
                    <DropdownMenu.Trigger asChild>
                      <button
                        type="button"
                        className="
                          flex h-9 w-9 items-center justify-center
                          rounded-lg text-slate-500
                          transition
                          hover:bg-slate-800
                          hover:text-slate-200
                        "
                      >
                        <MoreVertical className="h-4 w-4" />
                      </button>
                    </DropdownMenu.Trigger>

                    <DropdownMenu.Portal>
                      <DropdownMenu.Content
                        align="end"
                        sideOffset={8}
                        className="
                          z-50 min-w-[170px]
                          rounded-xl border border-slate-800
                          bg-[#0d111c]
                          p-1.5
                          shadow-2xl shadow-black/40
                        "
                      >
                        <DropdownMenu.Item onClick={() => handleOpenPlugin(plugin)} className="cursor-pointer rounded-lg px-3 py-2 text-sm text-slate-300 outline-none hover:bg-slate-800 focus:bg-slate-800">
                          Open
                        </DropdownMenu.Item>

                        <DropdownMenu.Item className="cursor-pointer rounded-lg px-3 py-2 text-sm text-slate-300 outline-none hover:bg-slate-800 focus:bg-slate-800">
                          Rename
                        </DropdownMenu.Item>

                        <DropdownMenu.Item className="cursor-pointer rounded-lg px-3 py-2 text-sm text-slate-300 outline-none hover:bg-slate-800 focus:bg-slate-800">
                          Duplicate
                        </DropdownMenu.Item>

                        <DropdownMenu.Separator className="my-1 h-px bg-slate-800" />

                        <DropdownMenu.Item className="cursor-pointer rounded-lg px-3 py-2 text-sm text-red-400 outline-none hover:bg-red-500/10 focus:bg-red-500/10">
                          Delete
                        </DropdownMenu.Item>
                      </DropdownMenu.Content>
                    </DropdownMenu.Portal>
                  </DropdownMenu.Root>
                </div>
              </CardHeader>

              <CardContent className="flex h-full flex-col">
                <p className="text-sm leading-6 text-slate-400">
                  {plugin.description}
                </p>

                <div className="mt-6 grid grid-cols-2 gap-4">
                  <div>
                    <p className="text-xs text-slate-600">
                      Executions
                    </p>

                    <p className="mt-1 font-mono text-sm text-slate-300">
                      {plugin.executions}
                    </p>
                  </div>

                  <div>
                    <p className="text-xs text-slate-600">
                      Avg runtime
                    </p>

                    <p className="mt-1 font-mono text-sm text-slate-300">
                      {plugin.runtime}
                    </p>
                  </div>
                </div>

                <div className="mt-6 flex items-center justify-between border-t border-slate-800/80 pt-4">
                  <p className="text-xs text-slate-600">
                    Updated {plugin.updated}
                  </p>

                  <button
                    type="button"
                    onClick={() => handleOpenPlugin(plugin)}
                    className="
                      flex items-center gap-2
                      text-sm font-medium
                      text-violet-400
                      transition
                      hover:text-violet-300
                    "
                  >
                    <Play className="h-3.5 w-3.5" />
                    Open
                  </button>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        ))}
      </section>
    </div>
  );
}

export default Plugins;