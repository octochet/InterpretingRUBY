#token types
INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF,ID, ASSIGN_OP, SEMI,STRING, EQUALS, LESSTHAN, GREATERTHAN, NOTEQUALS, LESSTHANEQUALS, GREATERTHANEQUALS = (
    'INTEGER', 'PLUS', 'MINUS', 'MUL', 'DIV', '(', ')', 'EOF', 'ID', 'ASSIGN_OP', 'SEMI', 'STRING', 'EQUALS', 'LESSTHAN', 'GREATERTHAN', 'NOTEQUALS', 'LESSTHANEQUALS', 'GREATERTHANEQUALS'
)


class Token(object):
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return 'Token({type}, {value})'.format(
            type=self.type,
            value=repr(self.value)
        )

    def __repr__(self):
        return self.__str__()

RESERVED_KEYWORDS = {
        'end': Token('END', 'END'),
        'if' : Token('IF', 'IF'),
        'else': Token('ELSE', 'ELSE'),
        'elsif': Token('ELSIF','ELSIF'),
        'then' : Token('THEN', 'THEN'),
        'while': Token('WHILE', 'WHILE'),
        'unless' : Token('UNLESS', 'UNLESS'),
        'do': Token('DO', 'DO'),
        'puts' : Token('PUTS', 'PUTS'),
        'until' : Token('UNTIL', 'UNTIL')
        
    }

class Lexer(object):
    def __init__(self, text):
        # client string input, e.g. "4 + 2 * 3 - 6 / 2"
        self.text = text
        # self.pos is an index into self.text
        self.pos = 0
        self.current_char = self.text[self.pos]

    def error(self):
        raise Exception('Invalid character')

    

    def peek(self):
        peek_pos = self.pos + 1
        if peek_pos > len(self.text) - 1:
            return None
        else:
            return self.text[peek_pos]


    def _id(self):
        """Handle identifiers and reserved keywords"""
        result = ''
        while self.current_char is not None and self.current_char.isalnum():
            result += self.current_char
            self.advance()
        token = RESERVED_KEYWORDS.get(result, Token(ID, result))
        return token


    def advance(self):
        """Advance the `pos` pointer and set the `current_char` variable."""
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_char = None  # Indicates end of input
        else:
            self.current_char = self.text[self.pos]

    def skip_whitespace(self):
        while self.current_char is not None and self.current_char.isspace():
            self.advance()

    def integer(self):
        """Return a (multi digit) integer consumed from the input."""
        result = ''
        while self.current_char is not None and self.current_char.isdigit():
            result += self.current_char
            self.advance()
        return int(result)

    def string(self):
        """Return a string from the input."""
        string=""
        while self.current_char is not None and self.current_char != '"':
            string += self.current_char
            self.advance()
        self.advance()
        return string
        
    def get_next_token(self):
        """Lexical analyzer (also known as scanner or tokenizer)

        This method is responsible for breaking a sentence
        apart into tokens. One token at a time.

        """
        while self.current_char is not None:

            if self.current_char.isspace():
                self.skip_whitespace()
                continue

            if self.current_char.isdigit():
                return Token(INTEGER, self.integer())
            
            if self.current_char.isalpha():
                return self._id()

            if self.current_char == '+':
                self.advance()
                return Token(PLUS, '+')
                
            if self.current_char == '"':
                self.advance()
                return Token(STRING,self.string())
                
            if self.current_char == '=':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(EQUALS, '==')
                return Token(ASSIGN_OP, '=')
            
            if self.current_char == ';':
                self.advance()
                return Token(SEMI, ';')

            if self.current_char == '-':
                self.advance()
                return Token(MINUS, '-')

            if self.current_char == '*':
                self.advance()
                return Token(MUL, '*')

            if self.current_char == '/':
                self.advance()
                return Token(DIV, '/')

            if self.current_char == '(':
                self.advance()
                return Token(LPAREN, '(')

            if self.current_char == ')':
                self.advance()
                return Token(RPAREN, ')')
            
                
            if self.current_char == '<':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(LESSTHANEQUALS, '<=')
                return Token(LESSTHAN, '<')
                
            if self.current_char == '>':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(GREATERTHANEQUALS, '>=')
                return Token(GREATERTHAN, '>')
                
            if self.current_char == '!':
                self.advance()
                if self.current_char == '=':
                    self.advance()
                    return Token(NOTEQUALS, '!=')
            


            self.error()

        return Token(EOF, None)

