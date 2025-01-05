from flask import Blueprint, request, jsonify
from typing import Dict, List
from ..parser.grammar import Grammar
from ..parser.lr1_parser import LR1Parser
import logging

logging.basicConfig(level=logging.DEBUG)

api = Blueprint('api', __name__)

@api.route("/parse", methods=["POST"])
def parse_input():
    try:
        input_data = request.get_json()
        logging.debug(f"Received input data: {input_data}")
        
        if 'grammar' not in input_data or 'start_symbol' not in input_data or 'input_string' not in input_data:
            return jsonify({"error": "Missing required fields"}), 400

        grammar = Grammar(
            productions=input_data['grammar'],
            start_symbol=input_data['start_symbol']
        )

        if not grammar.validate_grammar():
            return jsonify({"error": "Invalid grammar format"}), 400

        parser = LR1Parser(grammar)
        parser.build_parsing_table()
        parsing_steps = parser.parse_string(input_data['input_string'])

        lr1_sets = [
            {
                "state": i,
                "items": [
                    {
                        "non_terminal": item[0],
                        "production": item[1],
                        "dot_position": item[2],
                        "lookahead": item[3]
                    }
                    for item in item_set
                ]
            }
            for i, item_set in enumerate(parser.lr1_items)
        ]

        parsing_table = {
            f"{state}_{symbol}": {
                "action": action,
                "value": str(value)
            }
            for (state, symbol), (action, value) in parser.parsing_table.items()
        }

        return jsonify({
            "lr1_sets": lr1_sets,
            "parsing_table": parsing_table,
            "parsing_steps": parsing_steps
        })

    except Exception as e:
        logging.error(f"Error during parsing: {e}")
        return jsonify({"error": str(e)}), 400