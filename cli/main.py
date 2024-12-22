### File: `cli/main.py`

import sys
from compiler.lexer import Lexer
from compiler.parser import Parser
from compiler.transpiler import Transpiler
from runtime.simulator import Simulator
from runtime.executor import Executor

def main():
    """Main entry point for the MAQ CLI."""
    if len(sys.argv) != 2:
        print("Usage: python main.py <source_file.qp>")
        return

    # Read the MAQ source file
    source_file = sys.argv[1]
    try:
        with open(source_file, 'r') as f:
            code = f.read()
    except FileNotFoundError:
        print(f"Error: File '{source_file}' not found.")
        return

    # Step 1: Lexical Analysis
    lexer = Lexer(code)
    tokens = lexer.tokenize()

    # Step 2: Parsing
    parser = Parser(tokens)
    instructions, functions = parser.parse()

    # Step 3: Transpilation
    num_qubits = 5  # Adjust based on the input program's needs
    transpiler = Transpiler(instructions, functions, num_qubits)
    circuit = transpiler.transpile()

    # Step 4: Simulation
    simulator = Simulator(circuit)
    result = simulator.simulate()

    # Output the results
    print("Simulation Results:")
    for state, count in result.items():
        print(f"State: {state}, Count: {count}")

if __name__ == "__main__":
    main()
