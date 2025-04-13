import React from "react";

const StepWrapper = React.forwardRef(function StepWrapper({ children, visible }, ref) {
  if (!visible) return null;

  return (
    <div ref={ref} className="my-12">
      {children}
    </div>
  );
});

export default StepWrapper;