import React, { useState } from "react";
import { GrammarInput } from "./components/GrammarInput";
import { LR1SetsView } from "./components/LR1SetsView";
import { ParsingTable } from "./components/ParsingTable";
import { ParserSimulation } from "./components/ParserSimulation";
import { ParserInput, ParserResponse } from "./types"; // Correct import

const App: React.FC = () => {
  const [parserResponse, setParserResponse] = useState<ParserResponse | null>(
    null
  );
  const [error, setError] = useState<string>("");
  const [activeTab, setActiveTab] = useState<string>("lr1-sets");

  const handleParserInput = async (input: ParserInput) => {
    try {
      const response = await fetch("http://127.0.0.1:8001/api/parse", {
        // Ensure port is 8001
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          grammar: input.grammar.productions,
          start_symbol: input.grammar.start_symbol,
          input_string: input.input_string,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Failed to parse input");
      }

      const data = await response.json();
      setParserResponse(data);
      setError("");
    } catch (e) {
      setError(e instanceof Error ? e.message : "An error occurred");
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-6">LR(1) Parser</h1>

      <div className="space-y-6">
        <GrammarInput onSubmit={handleParserInput} />

        {error && (
          <div className="alert alert-destructive bg-red-100 text-red-700 p-2 rounded-lg">
            <div className="alert-description">{error}</div>
          </div>
        )}

        {parserResponse && (
          <div className="tabs">
            <div className="tabs-list flex space-x-4">
              <button
                className={`tabs-trigger px-4 py-2 rounded-lg ${
                  activeTab === "lr1-sets"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200"
                }`}
                onClick={() => setActiveTab("lr1-sets")}
              >
                LR(1) Sets
              </button>
              <button
                className={`tabs-trigger px-4 py-2 rounded-lg ${
                  activeTab === "parsing-table"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200"
                }`}
                onClick={() => setActiveTab("parsing-table")}
              >
                Parsing Table
              </button>
              <button
                className={`tabs-trigger px-4 py-2 rounded-lg ${
                  activeTab === "simulation"
                    ? "bg-blue-500 text-white"
                    : "bg-gray-200"
                }`}
                onClick={() => setActiveTab("simulation")}
              >
                Simulation
              </button>
            </div>

            {activeTab === "lr1-sets" && (
              <div className="tabs-content mt-4">
                <LR1SetsView sets={parserResponse.lr1_sets} />
              </div>
            )}

            {activeTab === "parsing-table" && (
              <div className="tabs-content mt-4">
                <ParsingTable table={parserResponse.parsing_table} />
              </div>
            )}

            {activeTab === "simulation" && (
              <div className="tabs-content mt-4">
                <ParserSimulation steps={parserResponse.parsing_steps} />
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default App;
