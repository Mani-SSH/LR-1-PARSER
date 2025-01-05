export interface Grammar {
  productions: Record<string, string[]>;
  start_symbol: string;
}

export interface ParserInput {
  grammar: Grammar;
  input_string: string;
}

export interface ParserResponse {
  lr1_sets: Array<{
    state: number;
    items: Array<{
      non_terminal: string;
      production: string;
      dot_position: number;
      lookahead: string;
    }>;
  }>;
  parsing_table: { [key: string]: { action: string; value: string } };
  parsing_steps: Array<{
    stack: Array<[number, string]>;
    input: string[];
    action: string;
    value: string;
  }>;
}
