# tests/lexer/test_lexer.py
from algolang.lexer import Lexer, LexerError, Token, TokenType

SRC = """
read n
read array a[n]
sort a
int lo = 0
int hi = n - 1
while lo < hi:
    int s = a[lo] + a[hi]
    if s == 0:
        print lo, hi
        break
    elif s < 0:
        lo = lo + 1
    else:
        hi = hi - 1
"""

def test_lexer_basic():
    tokens = Lexer(SRC).tokenize()
    for tok in tokens:
        print(tok)
    # basic assertions
    assert len(tokens) > 0
    assert tokens[-1].type == TokenType.EOF
    types = {t.type for t in tokens}
    assert TokenType.READ in types
    assert TokenType.WHILE in types
    assert TokenType.IF in types