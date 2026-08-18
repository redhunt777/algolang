# lexer/lexer.py

from .tokens import Token, TokenType

KEYWORDS = {
    'read':   TokenType.READ,
    'print':  TokenType.PRINT,
    'for':    TokenType.FOR,
    'while':  TokenType.WHILE,
    'if':     TokenType.IF,
    'elif':   TokenType.ELIF,
    'else':   TokenType.ELSE,
    'sort':   TokenType.SORT,
    'array':  TokenType.ARRAY,
    'in':     TokenType.IN,
    'int':    TokenType.INT,
    'int64':  TokenType.INT64,
    'break':  TokenType.BREAK,
    'return': TokenType.RETURN,
    'and':    TokenType.AND,
    'or':     TokenType.OR,
    'not':    TokenType.NOT,
}

class LexerError(Exception):
    def __init__(self, message, line, column):
        super().__init__(f"[LexerError] Line {line}, Col {column}: {message}")
        self.line = line
        self.column = column


class Lexer:
    def __init__(self, source: str):
        self.source = source
        self.pos = 0
        self.line = 1
        self.column = 1
        self.tokens: list[Token] = []
        self.indent_stack = [0]   # stack of indentation levels

    # ─── Core helpers ────────────────────────────────────────────────────────

    def peek(self, offset=0) -> str:
        """Look at character at current pos + offset without consuming."""
        idx = self.pos + offset
        return self.source[idx] if idx < len(self.source) else ''

    def advance(self) -> str:
        """Consume and return the current character."""
        ch = self.source[self.pos]
        self.pos += 1
        if ch == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
        return ch

    def match(self, expected: str) -> bool:
        """Consume next char only if it matches expected."""
        if self.pos < len(self.source) and self.source[self.pos] == expected:
            self.advance()
            return True
        return False

    def make_token(self, ttype: TokenType, value: str, line=None, col=None) -> Token:
        return Token(ttype, value, line or self.line, col or self.column)

    # ─── Indentation ─────────────────────────────────────────────────────────

    def handle_indent(self, indent_level: int, line: int):
        """
        Compare indent_level against the top of the indent stack and
        emit INDENT / DEDENT tokens accordingly.
        """
        current = self.indent_stack[-1]

        if indent_level > current:
            self.indent_stack.append(indent_level)
            self.tokens.append(self.make_token(TokenType.INDENT, '', line, 1))

        elif indent_level < current:
            while self.indent_stack[-1] > indent_level:
                self.indent_stack.pop()
                self.tokens.append(self.make_token(TokenType.DEDENT, '', line, 1))
            if self.indent_stack[-1] != indent_level:
                raise LexerError("Inconsistent indentation", line, 1)

    # ─── Tokenizers ──────────────────────────────────────────────────────────

    def read_number(self) -> Token:
        start_col = self.column
        num = ''
        is_float = False
        while self.peek().isdigit():
            num += self.advance()
        if self.peek() == '.' and self.peek(1) != '.':   # don't eat '..'
            is_float = True
            num += self.advance()
            while self.peek().isdigit():
                num += self.advance()
        ttype = TokenType.FLOAT if is_float else TokenType.INTEGER
        return self.make_token(ttype, num, self.line, start_col)

    def read_identifier(self) -> Token:
        start_col = self.column
        word = ''
        while self.peek().isalnum() or self.peek() == '_':
            word += self.advance()
        ttype = KEYWORDS.get(word, TokenType.IDENTIFIER)
        return self.make_token(ttype, word, self.line, start_col)

    def read_string(self) -> Token:
        start_col = self.column
        self.advance()   # opening "
        s = ''
        while self.peek() and self.peek() != '"':
            if self.peek() == '\n':
                raise LexerError("Unterminated string literal", self.line, start_col)
            s += self.advance()
        if not self.peek():
            raise LexerError("Unterminated string literal", self.line, start_col)
        self.advance()   # closing "
        return self.make_token(TokenType.STRING, s, self.line, start_col)

    # ─── Main tokenize loop ──────────────────────────────────────────────────

    def tokenize(self) -> list[Token]:
        lines = self.source.splitlines(keepends=True)

        for line_num, raw_line in enumerate(lines, start=1):
            self.line = line_num

            # --- measure indentation ---
            stripped = raw_line.lstrip(' \t')
            indent = len(raw_line) - len(stripped)
            content = stripped.rstrip('\n\r')

            # skip blank lines and comment-only lines
            if not content or content.startswith('//'):
                continue

            self.handle_indent(indent, line_num)
            self.column = indent + 1
            self.pos = sum(len(l) for l in lines[:line_num - 1]) + indent

            # --- lex the content of this line ---
            end_pos = self.pos + len(content)

            while self.pos < end_pos:
                ch = self.peek()

                # whitespace (mid-line)
                if ch in (' ', '\t'):
                    self.advance()
                    continue

                # comment
                if ch == '/' and self.peek(1) == '/':
                    break   # rest of line is a comment

                # number
                if ch.isdigit():
                    self.tokens.append(self.read_number())
                    continue

                # identifier or keyword
                if ch.isalpha() or ch == '_':
                    self.tokens.append(self.read_identifier())
                    continue

                # string literal
                if ch == '"':
                    self.tokens.append(self.read_string())
                    continue

                # two-character operators (must come before single-char)
                start_col = self.column
                if ch == '=' and self.peek(1) == '=':
                    self.advance(); self.advance()
                    self.tokens.append(self.make_token(TokenType.EQUAL_EQUAL, '==', line_num, start_col))
                elif ch == '!' and self.peek(1) == '=':
                    self.advance(); self.advance()
                    self.tokens.append(self.make_token(TokenType.NOT_EQUAL, '!=', line_num, start_col))
                elif ch == '<' and self.peek(1) == '=':
                    self.advance(); self.advance()
                    self.tokens.append(self.make_token(TokenType.LESS_EQUAL, '<=', line_num, start_col))
                elif ch == '>' and self.peek(1) == '=':
                    self.advance(); self.advance()
                    self.tokens.append(self.make_token(TokenType.GREATER_EQUAL, '>=', line_num, start_col))
                elif ch == '.' and self.peek(1) == '.':
                    self.advance(); self.advance()
                    self.tokens.append(self.make_token(TokenType.RANGE, '..', line_num, start_col))

                # single-character tokens
                elif ch == '+':  self.advance(); self.tokens.append(self.make_token(TokenType.PLUS,          '+', line_num, start_col))
                elif ch == '-':  self.advance(); self.tokens.append(self.make_token(TokenType.MINUS,         '-', line_num, start_col))
                elif ch == '*':  self.advance(); self.tokens.append(self.make_token(TokenType.STAR,          '*', line_num, start_col))
                elif ch == '/':  self.advance(); self.tokens.append(self.make_token(TokenType.SLASH,         '/', line_num, start_col))
                elif ch == '%':  self.advance(); self.tokens.append(self.make_token(TokenType.MOD,           '%', line_num, start_col))
                elif ch == '=':  self.advance(); self.tokens.append(self.make_token(TokenType.EQUAL,         '=', line_num, start_col))
                elif ch == '<':  self.advance(); self.tokens.append(self.make_token(TokenType.LESS,          '<', line_num, start_col))
                elif ch == '>':  self.advance(); self.tokens.append(self.make_token(TokenType.GREATER,       '>', line_num, start_col))
                elif ch == '(':  self.advance(); self.tokens.append(self.make_token(TokenType.LEFT_PAREN,    '(', line_num, start_col))
                elif ch == ')':  self.advance(); self.tokens.append(self.make_token(TokenType.RIGHT_PAREN,   ')', line_num, start_col))
                elif ch == '[':  self.advance(); self.tokens.append(self.make_token(TokenType.LEFT_BRACKET,  '[', line_num, start_col))
                elif ch == ']':  self.advance(); self.tokens.append(self.make_token(TokenType.RIGHT_BRACKET, ']', line_num, start_col))
                elif ch == ':':  self.advance(); self.tokens.append(self.make_token(TokenType.COLON,         ':', line_num, start_col))
                elif ch == ',':  self.advance(); self.tokens.append(self.make_token(TokenType.COMMA,         ',', line_num, start_col))
                else:
                    self.advance()
                    self.tokens.append(self.make_token(TokenType.UNKNOWN, ch, line_num, start_col))

            # end of line → emit NEWLINE
            self.tokens.append(self.make_token(TokenType.NEWLINE, '', line_num, len(raw_line)))

        # flush remaining indentation levels
        while len(self.indent_stack) > 1:
            self.indent_stack.pop()
            self.tokens.append(self.make_token(TokenType.DEDENT, '', self.line, 1))

        self.tokens.append(self.make_token(TokenType.EOF, '', self.line, self.column))
        return self.tokens