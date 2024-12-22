import re

class Lexer:
    """Lexical analyzer for MAQ code."""
    def __init__(self, code):
        self.code = code  # Input code to tokenize
        self.tokens = []  # List to store the tokens

    def tokenize(self):
        """Tokenizes the input code into lexemes."""
        patterns = [
            (r'def', 'DEF'),  # Function definition
            (r'end', 'END'),  # Function end
            (r'return', 'RETURN'),  # Return statement
            (r'IF', 'IF'),  # Conditional statement
            (r'THEN', 'THEN'),  # Conditional action
            (r'[a-zA-Z_][a-zA-Z0-9_]*', 'IDENTIFIER'),  # Identifiers
            (r'\d+', 'NUMBER'),  # Numbers
            (r'\(', 'LPAREN'),  # Opening parenthesis
            (r'\)', 'RPAREN'),  # Closing parenthesis
            (r';', 'SEMICOLON'),  # Semicolon
            (r'H', 'HADAMARD'),  # Hadamard gate
            (r'CNOT', 'CNOT'),  # CNOT gate
            (r'MEASURE', 'MEASURE'),  # Measurement
        ]
        # Match each pattern and generate tokens
        for pattern, token_type in patterns:
            for match in re.finditer(pattern, self.code):
                self.tokens.append((token_type, match.group()))
        return self.tokens
