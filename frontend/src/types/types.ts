export interface Grammar {
  productions: Record<string, string[]>;
  start_symbol: string;
}

export interface ParserInput {
  grammar: Grammar;
  input_string: string;
}

export interface LR1Item {
  non_terminal: string;
  production: string;
  dot_position: number;
  lookahead: string;
}

export interface LR1State {
  state: number;
  items: LR1Item[];
}

export interface ParsingTableEntry {
  action: string;
  value: string;
}

export interface ParsingStep {
  stack: [number, string][];
  input: string[];
  action: string;
  value: string;
}

export interface ParserResponse {
  lr1_sets: LR1State[];
  parsing_table: Record<string, ParsingTableEntry>;
  parsing_steps: ParsingStep[];
}
