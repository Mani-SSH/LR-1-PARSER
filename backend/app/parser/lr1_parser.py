from typing import Dict, Set, List, Tuple
from pydantic import BaseModel
import logging

class Grammar(BaseModel):
    productions: Dict[str, List[str]]
    start_symbol: str

class ParserState:
    def __init__(self):
        self.lr1_items: Set[Tuple[str, str, int, str]] = set()  # (non-terminal, production, dot_position, lookahead)
        self.parsing_table: Dict[Tuple[int, str], Tuple[str, int]] = {}  # (state, symbol) -> (action, next_state)
        
    def compute_lr1_sets(self, grammar: Grammar):
        # Initialize with start item
        start_prod = grammar.productions[grammar.start_symbol][0]
        self.lr1_items.add((grammar.start_symbol, start_prod, 0, "$"))
        
        # Compute closure and goto sets (simplified for example)
        # In a real implementation, you would add the full LR(1) set computation here
        pass

    def build_parsing_table(self):
        # Build the parsing table from LR(1) sets
        # In a real implementation, you would add the full parsing table construction here
        pass

    def parse_string(self, input_string: str) -> List[str]:
        # Simulate parsing using the parsing table
        # Returns the sequence of steps in the parsing process
        steps = []
        # Add actual parsing logic here
        return steps

class LR1Parser:
    def __init__(self, grammar: Grammar):
        self.grammar = grammar
        self.lr1_items: List[Set[Tuple[str, str, int, str]]] = []  # List of sets of LR(1) items
        self.parsing_table: Dict[Tuple[int, str], Tuple[str, int]] = {}  # (state, symbol) -> (action, next_state)
        self.goto_table: Dict[Tuple[int, str], int] = {}  # (state, non-terminal) -> next_state

    def compute_closure(self, items: Set[Tuple[str, str, int, str]]) -> Set[Tuple[str, str, int, str]]:
        """Compute closure of a set of LR(1) items"""
        closure = items.copy()
        changed = True
        first_sets = self.grammar.get_first_sets()

        while changed:
            changed = False
            new_items = set()

            for item in closure:
                non_terminal, production, dot_pos, lookahead = item
                if dot_pos >= len(production.split()):
                    continue

                symbols = production.split()
                next_symbol = symbols[dot_pos]

                if next_symbol in self.grammar.non_terminals:
                    # Calculate first set of remaining symbols plus lookahead
                    remaining = symbols[dot_pos + 1:] + [lookahead]
                    first = set()
                    all_nullable = True

                    for symbol in remaining:
                        symbol_first = first_sets.get(symbol, {symbol})
                        first |= {s for s in symbol_first if s != ''}
                        if '' not in symbol_first:
                            all_nullable = False
                            break

                    if all_nullable:
                        first.add(lookahead)

                    # Add items for the non-terminal
                    for prod in self.grammar.productions[next_symbol]:
                        for look in first:
                            new_item = (next_symbol, prod, 0, look)
                            if new_item not in closure:
                                new_items.add(new_item)
                                changed = True

            closure |= new_items

        return closure

    def compute_goto(self, items: Set[Tuple[str, str, int, str]], symbol: str) -> Set[Tuple[str, str, int, str]]:
        """Compute GOTO for a set of items and a grammar symbol"""
        goto_items = set()

        for item in items:
            non_terminal, production, dot_pos, lookahead = item
            symbols = production.split()

            if dot_pos < len(symbols) and symbols[dot_pos] == symbol:
                goto_items.add((non_terminal, production, dot_pos + 1, lookahead))

        return self.compute_closure(goto_items)

    def build_lr1_sets(self):
        """Build the collection of LR1 item sets"""
        # Initialize with augmented grammar start item
        augmented_start_symbol = f"{self.grammar.start_symbol}'"
        augmented_start_production = f"{self.grammar.start_symbol}"
        start_item = (augmented_start_symbol, augmented_start_production, 0, '$')
        
        # Add the augmented start production to the grammar
        self.grammar.productions[augmented_start_symbol] = [augmented_start_production]
        self.grammar.non_terminals.add(augmented_start_symbol)
        
        initial_set = self.compute_closure({start_item})
        
        # Ensure the initial set is always set 1
        self.lr1_items = [set(), initial_set]
        processed = {1}
        
        while True:
            new_sets = []
            
            for i, item_set in enumerate(self.lr1_items):
                if i in processed:
                    continue
                    
                processed.add(i)
                symbols = self.grammar.terminals | self.grammar.non_terminals
                
                for symbol in symbols:
                    goto_set = self.compute_goto(item_set, symbol)
                    if not goto_set:
                        continue
                        
                    if goto_set not in self.lr1_items:
                        new_sets.append(goto_set)
                        next_state = len(self.lr1_items) + len(new_sets) - 1
                        if symbol.islower() or symbol == '$':
                            self.parsing_table[(i, symbol)] = ('shift', next_state)
                        else:
                            self.goto_table[(i, symbol)] = next_state
                    else:
                        next_state = self.lr1_items.index(goto_set)
                        if symbol.islower() or symbol == '$':
                            self.parsing_table[(i, symbol)] = ('shift', next_state)
                        else:
                            self.goto_table[(i, symbol)] = next_state
                            
            if not new_sets:
                break
                
            self.lr1_items.extend(new_sets)

    def build_parsing_table(self):
        """Build the LR(1) parsing table"""
        self.build_lr1_sets()
        
        # Add reduce actions
        for i, item_set in enumerate(self.lr1_items):
            for item in item_set:
                non_terminal, production, dot_pos, lookahead = item
                symbols = production.split()
                
                if dot_pos == len(symbols):  # Reduce item
                    if non_terminal == f"{self.grammar.start_symbol}'" and lookahead == '$':
                        self.parsing_table[(i, '$')] = ('accept', 0)
                    else:
                        self.parsing_table[(i, lookahead)] = ('reduce', 
                            (non_terminal, production))
        
        logging.debug(f"Parsing table: {self.parsing_table}")

    def parse_string(self, input_string: str) -> List[dict]:
        """Parse an input string and return the steps of the parsing process"""
        logging.debug(f"Starting to parse input string: {input_string}")
        try:
            if not self.parsing_table:
                self.build_parsing_table()

            steps = []
            stack = [(0, '$')]  # (state, symbol)
            symbols = self.tokenize(input_string) + ['$']
            cursor = 0

            while True:
                current_state = stack[-1][0]
                current_symbol = symbols[cursor]
                logging.debug(f"Current state: {current_state}, Current symbol: {current_symbol}")

                if (current_state, current_symbol) not in self.parsing_table:
                    raise ValueError(f"Parsing error at symbol {current_symbol}")

                action, value = self.parsing_table[(current_state, current_symbol)]
                steps.append({
                    'stack': [(s, sym) for s, sym in stack],
                    'input': symbols[cursor:],
                    'action': action,
                    'value': str(value)
                })

                if action == 'shift':
                    stack.append((value, current_symbol))
                    cursor += 1
                elif action == 'reduce':
                    non_terminal, production = value
                    num_symbols = len(production.split())
                    for _ in range(num_symbols):
                        stack.pop()
                    prev_state = stack[-1][0]
                    next_state = self.goto_table[(prev_state, non_terminal)]
                    stack.append((next_state, non_terminal))
                elif action == 'accept':
                    break
                else:
                    raise ValueError(f"Invalid action: {action}")

            for step in steps:
                logging.debug(f"Parsing step: {step}")

        except Exception as e:
            logging.error(f"Error during parsing: {e}")
            raise e

        return steps

    def tokenize(self, input_string: str) -> List[str]:
        """Tokenize the input string into individual symbols"""
        tokens = []
        current_token = ""
        for char in input_string:
            if char.isalnum():
                current_token += char
            else:
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                if char.strip():
                    tokens.append(char)
        if current_token:
            tokens.append(current_token)
        return tokens