# tokens/tokens.py


from enum import Enum, auto
from dataclasses import dataclass


class TokenType(Enum):
    # Keywords
    READ = auto()
    PRINT = auto()
    FOR = auto()
    WHILE = auto()
    IF = auto()
    ELIF = auto()
    ELSE = auto()
    SORT = auto()
    ARRAY = auto()
    IN = auto()
    INT = auto()
    INT64 = auto()
    BREAK = auto()
    RETURN = auto()
    AND = auto()
    OR = auto()
    NOT = auto()

    # Literals / identifiers
    IDENTIFIER = auto()
    INTEGER = auto()
    FLOAT = auto()
    STRING = auto()

    # Operators
    PLUS = auto()
    MINUS = auto()
    STAR = auto()
    SLASH = auto()
    MOD = auto()
    EQUAL = auto()
    EQUAL_EQUAL = auto()
    LESS = auto()
    GREATER = auto()
    LESS_EQUAL = auto()
    GREATER_EQUAL = auto()
    NOT_EQUAL = auto()

    # Symbols
    LEFT_PAREN = auto()
    RIGHT_PAREN = auto()
    LEFT_BRACKET = auto()
    RIGHT_BRACKET = auto()
    COLON = auto()
    COMMA = auto()
    RANGE = auto()       # ..

    # Indentation
    INDENT = auto()
    DEDENT = auto()

    NEWLINE = auto()
    EOF = auto()
   
    UNKNOWN = auto()      # Useful for richer error recovery


@dataclass
class Token:
    type: TokenType
    value: str
    line: int
    column: int

    def __repr__(self):
        return f"Token({self.type.name}, {self.value!r}, {self.line}:{self.column})"