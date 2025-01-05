import React from "react";
import { LR1State } from "../types"; // Ensure this import is present

interface LR1SetsViewProps {
  sets: LR1State[];
}

export const LR1SetsView: React.FC<LR1SetsViewProps> = ({ sets }) => {
  return (
    <div className="card w-full shadow-lg rounded-lg">
      <div className="card-header bg-purple-500 text-white p-4 rounded-t-lg">
        <h2 className="card-title text-xl font-bold">LR(1) Sets</h2>
      </div>
      <div className="card-content p-4">
        <div className="space-y-4">
          {sets.map((stateSet) => (
            <div
              key={stateSet.state}
              className="border rounded-lg p-4 bg-gray-50"
            >
              <h3 className="font-medium mb-2">State {stateSet.state}</h3>
              <div className="space-y-2">
                {stateSet.items.map((item, index) => (
                  <div
                    key={index}
                    className="font-mono text-sm bg-white p-2 rounded-lg shadow-inner"
                  >
                    {item.non_terminal} →{" "}
                    {item.production
                      .split(" ")
                      .map((symbol, i) =>
                        i === item.dot_position ? "•" + symbol : symbol
                      )
                      .join(" ")}
                    , {item.lookahead}
                  </div>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};
