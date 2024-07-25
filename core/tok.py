import enum
import typing as ty


class TokenTypes(enum.Enum):
    """
    Class containing all token types with values to identify them.
    """
    # Basic
    INVALID = -1
    EOF = 0
    INIT = 1
    ATTR = 2
    PROGDECL = 3
    PLACEHOLDER = 4

    # Arithmetic operators
    PLUS = 101
    MINUS = 102
    ASTERISK = 103
    FSLASH = 104
    CARET = 105

    # Assignment and comparison operators
    EQ = 201
    EQEQ = 202
    NOTEQ = 203
    LT = 204
    LTEQ = 205
    GT = 206
    GTEQ = 207

    # Keywords (data types)
    INT = 301
    FLOAT = 302
    STRING = 303
    BOOL = 304
    IDENT = 305
    KEYWD = 340
    # Keywords (others)
    LET = 341
    IF = 342
    ELIF = 343
    ELSE = 344
    WHILE = 345
    FOR = 346
    FUN = 347
    RETURN = 348
    PRINT = 349
    SCAN = 350
    RAISE = 351

    # Other symbols
    LPAREN = 401
    RPAREN = 402
    LFLOBRAC = 403
    RFLOBRAC = 404
    LSQBRAC = 405
    RSQBRAC = 406
    SEMICLN = 407
    COLON = 408
    COMMA = 409

    # Program declarations
    STATIC = 501
    DYNAMIC = 502


class TokenLiterals(enum.Enum):
    """
    Class containing all token literals with values to identify them.
    """
    # Basic
    EOF = '\0'
    
    # Arithmetic operators
    PLUS = '+'
    MINUS = '-'
    ASTERISK = '*'
    FSLASH = '/'
    CARET = '^'

    # Assignment and comparison operators
    EQ = '='
    EQEQ = '=='
    NOTEQ = '!='
    LT = '<'
    LTEQ = '<='
    GT = '>'
    GTEQ = '>='

    # Other symbols
    LPAREN = '('
    RPAREN = ')'
    LFLOBRAC = '{'
    RFLOBRAC = '}'
    LSQBRAC = '['
    RSQBRAC = ']'
    SEMICLN = ';'


class Token:
    def __init__(self, typ:TokenTypes, val:str, line:int, pos:int, printPos:int|tuple, size:int) -> None:
        self.typ:TokenTypes = typ
        self.val:str = val
        self.line:int = line
        self.pos:int = pos
        self.printPos:int|ty.Tuple[int] = printPos
        self.size:int = size
    
    def __repr__(self) -> str:
        return f"Token[Typ({self.typ.name}): Val({self.val}): Line({self.line}): Pos({self.pos}): PrintPos({self.printPos}): Size({self.size})]"
    
    def __str__(self) -> str:
        val = '\'' + self.val + '\''
        return f"Type={self.typ.name:<8} : Value={val:<10} : Line={self.line:<2} : PrintPos={self.printPos} : Size={self.size}"
