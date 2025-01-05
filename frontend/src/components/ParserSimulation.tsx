import React from "react";
import { ParsingStep } from "../types";

interface ParserSimulationProps {
  steps: ParsingStep[];
}

export const ParserSimulation: React.FC<ParserSimulationProps> = ({
  steps,
}) => {
  return (
    <div className="card w-full shadow-lg rounded-lg">
      <div className="card-header bg-green-500 text-white p-4 rounded-t-lg">
        <h2 className="card-title text-xl font-bold">Parsing Steps</h2>
      </div>
      <div className="card-content p-4">
        <div className="space-y-4">
          {steps.map((step, index) => (
            <div key={index} className="border rounded-lg p-4 bg-gray-50">
              <div className="grid grid-cols-2 gap-4">
                <div>
                  <h4 className="font-medium mb-2">Stack</h4>
                  <div className="font-mono text-sm bg-white p-2 rounded-lg shadow-inner">
                    {step.stack.map(([state, symbol], i) => (
                      <span key={i} className="inline-block mr-1">
                        {state}
                        {symbol}{" "}
                      </span>
                    ))}
                  </div>
                </div>
                <div>
                  <h4 className="font-medium mb-2">Input</h4>
                  <div className="font-mono text-sm bg-white p-2 rounded-lg shadow-inner">
                    {step.input.join(" ")}
                  </div>
                </div>
              </div>
              <div className="mt-2">
                <h4 className="font-medium mb-2">Action</h4>
                <div className="font-mono text-sm bg-white p-2 rounded-lg shadow-inner">
                  {step.action} {step.value}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
