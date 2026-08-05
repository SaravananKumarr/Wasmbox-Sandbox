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
              z-50 rounded-lg border border-blue-100
              bg-white px-3 py-2
              text-xs text-slate-700 shadow-lg shadow-slate-200
            "
          >
            {content}

            <TooltipPrimitive.Arrow className="fill-white" />
          </TooltipPrimitive.Content>
        </TooltipPrimitive.Portal>
      </TooltipPrimitive.Root>
    </TooltipPrimitive.Provider>
  );
}

export default Tooltip;