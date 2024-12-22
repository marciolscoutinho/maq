class Parser:
    """Parses MAQ tokens into instructions and function definitions."""
    def __init__(self, tokens):
        self.tokens = tokens  # Input tokens
        self.pos = 0  # Current position in tokens

    def parse(self):
        """Parses the tokens into instructions and functions."""
        instructions = []
        functions = {}

        while self.pos < len(self.tokens):
            token = self.tokens[self.pos]
            if token[0] == 'DEF':  # Detect a function definition
                func_name = self.tokens[self.pos + 1][1]
                params = []
                self.pos += 2
                if self.tokens[self.pos][0] == 'LPAREN':  # Parse parameters
                    self.pos += 1
                    while self.tokens[self.pos][0] != 'RPAREN':
                        params.append(self.tokens[self.pos][1])
                        self.pos += 1
                    self.pos += 1
                func_body = []
                while self.tokens[self.pos][0] != 'END':
                    func_body.append(self.parse_instruction())
                self.pos += 1  # Skip 'END'
                functions[func_name] = {'params': params, 'body': func_body}
            else:
                instructions.append(self.parse_instruction())

        return instructions, functions

    def parse_instruction(self):
        """Parses an individual instruction."""
        token = self.tokens[self.pos]
        if token[0] == 'HADAMARD':
            qubit = self.tokens[self.pos + 1][1]
            self.pos += 2
            return ('H', int(qubit))
        elif token[0] == 'CNOT':
            control = self.tokens[self.pos + 1][1]
            target = self.tokens[self.pos + 2][1]
            self.pos += 3
            return ('CNOT', int(control), int(target))
        elif token[0] == 'MEASURE':
            qubit = self.tokens[self.pos + 1][1]
            self.pos += 2
            return ('MEASURE', int(qubit))
        elif token[0] == 'IF':
            self.pos += 1
            qubit = self.tokens[self.pos][1]
            self.pos += 1
            if self.tokens[self.pos][0] == 'THEN':
                self.pos += 1
                action = self.parse_instruction()
                return ('IF', int(qubit), action)
        elif token[0] == 'RETURN':
            self.pos += 1
            return ('RETURN', self.tokens[self.pos][1])
