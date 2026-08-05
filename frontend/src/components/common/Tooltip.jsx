import * as TooltipPrimitive from "@radix-ui/react-tooltip";

function Tooltip({ children, content }) {
  return (
    <TooltipPrimitive.Provider delayDuration={200}>
      <TooltipPrimitive.Root>
        <TooltipPrimitive.Trigger asChild>
          {children}
        </TooltipPrimitive.Trigger>

        <TooltipPrimitive.Portal>
          <TooltipPrimitive.Content
            sideOffset={8}
            className="
              z-50 rounded-lg border border-slate-700
              bg-slate-900 px-3 py-2
              text-xs text-slate-200 shadow-xl
            "
          >
            {content}

            <TooltipPrimitive.Arrow className="fill-slate-900" />
          </TooltipPrimitive.Content>
        </TooltipPrimitive.Portal>
      </TooltipPrimitive.Root>
    </TooltipPrimitive.Provider>
  );
}

export default Tooltip;