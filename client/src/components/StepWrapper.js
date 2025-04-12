import React from "react";

function StepWrapper({ visible, children }) {
  return (
    <div className={`step-transition ${visible ? "step-visible" : "step-hidden"}`}>
      {visible ? children : null}
    </div>
  );
}

export default StepWrapper;