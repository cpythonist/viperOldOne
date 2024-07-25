import sys
import typing as ty

import commons as comm
import err
import other as ot
import parse
import tok

# Please note TT is defined here!
TTn = tok.Token
TT = tok.TokenTypes
ANSI = comm.ANSI


class ASTNode:
    def __init__(self, parser:parse.Parser) -> None:
        self.parser = parser
    
    def __error(self, errType:ty.Type[err.Error], *args:ty.Any, **kwargs:ty.Any):
        sys.stdout.write(f"{ot.RED if ANSI else ''}??{ot.RESET if ANSI else ''} " + str(errType(*args, **kwargs)) + '\n')
        sys.stdout.flush()


class StatementNode(ASTNode):
    def __init__(self, statement, nextStatement=None) -> None:
        self.statement = statement
        self.nextStatement = nextStatement
    
    def __repr__(self) -> str:
        return f"StatementNode({self.statement}, {self.nextStatement})"


class BinOpNode(ASTNode):
    def __init__(self, left:ty.Any, op:str, right:ty.Any, leftType:TT, rightTyp:TT) -> None:
        self.err:bool = False
        self.leftTyp:TT = leftType
        self.rightTyp:TT = rightTyp

        if leftType != rightTyp:
            self.__error(err.typeErr, self.parser.token, self.parser.lexer.line, self.parser.lexer.printPos-self.parser.token.size)
            self.err = True
        
        else:
            self.left:ty.Any = left
            self.op:str = op
            self.right:str = right
    
    def __repr__(self) -> str:
        return f"BinOp({self.left}, {self.op}, {self.right}, type=({self.leftTyp}, {self.rightTyp}))"


class UnaryOpNode(ASTNode):
    def __init__(self, op:str, operand:str) -> None:
        self.op:str = op
        self.operand:str = operand
        self.typ:None = None
    
    def __repr__(self) -> str:
        return f"UnaryNode({self.op}, {self.operand}, type={self.typ})"

class NumNode(ASTNode):
    def __init__(self, val:int|float, typ:TT) -> None:
        self.val:int|float = val
        self.typ:TT = typ
    
    def __repr__(self) -> str:
        return f"NumNode({self.val}, type={self.typ.name})"


class IdentNode(ASTNode):
    def __init__(self, name:str, typ:TT) -> None:
        self.name:str = name
        self.typ:TT = typ
    
    def __repr__(self) -> str:
        return f"IdentNode({self.name}, type={self.typ.name})"


class LetNode(ASTNode):
    def __init__(self, ident:IdentNode, val:ty.Any, typ:TT) -> None:
        self.ident:IdentNode = ident
        self.val:ty.Any = val
        self.typ:TT = typ
    
    def __repr__(self) -> str:
        return f"AssignNode({self.ident}, {self.val}, type={self.typ.name})"


class IfNode(ASTNode):
    def __init__(self, condition, thenBranch, elseBranch=None) -> None:
        self.condition = condition
        self.thenBranch = thenBranch
        # self.elifBranches = elifBranches
        self.elseBranch = elseBranch
    
    def __repr__(self) -> str:
        return f"IfNode({self.condition}, then={self.thenBranch}, else={self.elseBranch})"


class WhileNode(ASTNode):
    def __init__(self, condition, thenBranch) -> None:
        self.condition = condition
        self.thenBranch = thenBranch
    
    def __repr__(self) -> str:
        return f"WhileNode({self.condition}, then={self.thenBranch})"


class ForNode(ASTNode):
    def __init__(self, iterable, thenBranch) -> None:
        self.iterable = iterable
        self.thenBranch = thenBranch
    
    def __repr__(self) -> str:
        return f"IfNode({self.iterable}, then={self.thenBranch})"


class FunNode(ASTNode):
    def __init__(self, name, parameters, body) -> None:
        self.name = name
        self.parameters = parameters
        self.body = body
    
    def __repr__(self) -> str:
        return f"FunNode({self.name}, {self.parameters}, {self.body})"
