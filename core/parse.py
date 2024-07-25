# TODO:
# 1. Implement dynamic typing system
# 2. Implement for loops
# 3. __expr correct it, return False for True comparisons

import inspect # For debugging
import operator
import sys
import typing as ty

import basicTypes as bt
import commons as comm
import err
import lex
import other as ot
import tok

# TT is defined here!
TT = tok.TokenTypes
inf = float("inf")
nan = float("nan")
ANSI = comm.ANSI
ops = {
    '+': operator.add,
    '-': operator.sub,
    '*': operator.mul,
    '/': operator.truediv,
    '^': operator.pow,
    '%': operator.mod,
    '==': operator.eq,
    '!=': operator.ne,
    '<': operator.lt,
    '<=': operator.le,
    '>': operator.gt,
    '>=': operator.ge,
    '+=': operator.iadd,
    '-=': operator.isub,
    '*=': operator.imul,
    '/=': operator.itruediv,
}


class Parser:
    def __init__(self, lexer:lex.Lexer) -> None:
        self.lexer:lex.Lexer = lexer
        self.token:tok.Token = tok.Token(TT.INIT, '', -1, -1, -1, 0)
        self.peekToken:tok.Token = tok.Token(TT.INIT, '', -1, -1, -1, 0)
        self.tokNum:int = 0 # aka parPos (for parser position)
        self.symTable:ty.Dict[str, ty.Any] = {}
        self.funcTable:ty.Dict[str, ty.Dict[str, str]] = {}
        self.typing:int = self.lexer.programTyping if self.lexer.programTyping != None else 0 # 0 for static, 1 for dynamic

        self.__readToken()
        self.__readToken()
    
    def __readToken(self) -> tok.Token:
        if self.token.typ != TT.EOF:
            self.token = self.peekToken
            self.peekToken = self.lexer.tokenize()
            self.tokNum += 1
        
        return self.token
    
    def __checkToken(self, tokTyp:TT, tokVal:ty.Any=None) -> bool:
        return (self.token.typ == tokTyp) and ((tokVal == None) or (self.token.val == tokVal))
    
    def __matchToken(self, tokTyp:TT, tokVal:str|None=None, error:ty.Type[err.Error]|None=None) -> None:
        if (tokTyp == TT.PLACEHOLDER) and (tokVal != None):
            if self.token.val != tokVal:
                self.__error(
                    err.syntaxErr if error == None else error,
                    self.token, self.lexer.line, self.lexer.printPos,
                    msg=f"Expected \"{tokVal}\", got \"{self.token.val}\" at line {self.lexer.line} pos {self.lexer.printPos-self.token.size}."
                )
            else:
                self.__readToken()
        
        elif not self.__checkToken(tokTyp, tokVal):
            self.__error(
                err.syntaxErr if error == None else error,
                self.token, self.lexer.line, self.lexer.printPos,
                msg=f"Expected {tokTyp.name}, got \"{self.token.val}\" ({self.token.typ.name}) at line {self.lexer.line} pos {self.lexer.printPos-self.token.size}."
            )
        elif self.__checkToken(tokTyp, tokVal):
            self.__readToken()
        
        else:
            err.fatalErr()
    
    def __error(self, errType:ty.Type[err.Error], *args:ty.Any, readToken:bool=True, **kwargs:ty.Any) -> None:
        "Displays errors."
        sys.stdout.write(f"{ot.RED if ANSI else ''}??{ot.RESET if ANSI else ''} " + str(errType(*args, **kwargs)) + '\n')
        sys.stdout.flush()
        self.__readToken() if readToken else None
    
    def parse(self):
        print(f"Typing: {'dynamic' if self.typing else 'static'}")
        print("PROGRAM-START")
        
        while (not self.__checkToken(TT.EOF)):
            self.__statement()
        
        print("PROGRAM-END")
    
    def __statement(self):
        if (self.__checkToken(TT.KEYWD, "print")):
            self.__print()
        
        elif (self.__checkToken(TT.KEYWD, "if")):
            self.__if()
        
        elif (self.__checkToken(TT.KEYWD, "while")):
            self.__while()
        
        elif (self.__checkToken(TT.KEYWD, "for")):
            self.__for()
        
        elif (self.__checkToken(TT.KEYWD, "let")):
            self.__let()
        
        elif (self.__checkToken(TT.KEYWD, "fun")):
            self.__fun()
        
        else:
            self.__error(err.syntaxErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size,
                         f"Unexpected token \"{self.token.val}\" (type {self.token.typ.name}) on line {self.lexer.line} pos {self.lexer.printPos-self.token.size}.")
            while (not self.__checkToken(TT.SEMICLN)):
                if self.__checkToken(TT.EOF):
                    break
                self.__readToken()

        self.__matchToken(TT.SEMICLN)
        while self.token.typ == TT.SEMICLN:
            self.__matchToken(TT.SEMICLN)
    
    def __print(self):
        print("KEYWD: print")
        self.__matchToken(TT.KEYWD, "print")

        # String or expression
        if self.__checkToken(TT.STRING):
            print(f"STRING: {self.token.val}")
            self.__matchToken(TT.STRING)
        
        else:
            result:int|float|bool|None = self.__expr()
            
            if result == None:
                self.__error(err.exprErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size, readToken=False)
                return
            
            # invalid:bool = False

            # if result == None:
            #     invalid = True
            
            # if self.isComparisonOp(self.token):
            #     comp = self.token.val
            #     self.__readToken()
            #     result2:int|float|None = self.__expr()

            #     if result2 == None:
            #         return
            #     if not invalid:
            #         print("COMPARISON:", ops[comp](result, result2))
            
            # else:

            print("EXPRESSION:", result)
    
    def __if(self):
        # if block
        invIfCondition:bool = False
        invElifCondition:bool = False

        print("KEYWD: if")
        self.__matchToken(TT.KEYWD, "if")
        self.__matchToken(TT.LPAREN)

        result = self.__expr()
        if result == None:
            invIfCondition = True
        
        self.__matchToken(TT.RPAREN)
        self.__matchToken(TT.LFLOBRAC)

        while not self.__checkToken(TT.RFLOBRAC):
            self.__statement()
        self.__matchToken(TT.RFLOBRAC)

        if not invIfCondition:
            if ot.evaluate(result):
                print("IF-block will be executed!")
            else:
                print("IF-block will NOT be executed!")
        
        # elif block
        elifCount = 0
        while self.__checkToken(TT.KEYWD, "elif"):
            print("KEYWD: elif")
            self.__matchToken(TT.KEYWD, "elif")
            self.__matchToken(TT.LPAREN)

            result = self.__expr()
            if result == None:
                invElifCondition = True
            
            self.__matchToken(TT.RPAREN)
            self.__matchToken(TT.LFLOBRAC)

            while not self.__checkToken(TT.RFLOBRAC):
                self.__statement()
            
            self.__matchToken(TT.RFLOBRAC)
            elifCount += 1
            
            if not invElifCondition:
                if ot.evaluate(result):
                    print(f"ELIF-block ({elifCount}) will be executed!")
                else:
                    print(f"ELIF-block ({elifCount}) will NOT be executed!")
        
        # else block
        if self.__checkToken(TT.KEYWD, "else"):
            print("KEYWD: else")
            self.__matchToken(TT.KEYWD, "else")
            self.__matchToken(TT.LFLOBRAC)
            
            while not self.__checkToken(TT.RFLOBRAC):
                self.__statement()
            
            self.__matchToken(TT.RFLOBRAC)

    def __while(self):
        invWhileCond:bool = False

        print("KEYWD: while")
        self.__matchToken(TT.KEYWD, "while")
        self.__matchToken(TT.LPAREN)
        
        result = self.__expr()
        if result == None:
            invWhileCond = True
        
        self.__matchToken(TT.RPAREN)
        self.__matchToken(TT.LFLOBRAC)

        while not self.__checkToken(TT.RFLOBRAC):
            self.__statement()
        
        self.__matchToken(TT.RFLOBRAC)

        if not invWhileCond:
            if ot.evaluate(result):
                print("WHILE-block will be executed!")
            else:
                print("WHILE-block will NOT be executed!")

    def __for(self):
        # TODO: Implement for loop
        pass

    def __let(self):
        print("KEYWD: let")
        self.__matchToken(TT.KEYWD, "let")

        if ((self.token.val.upper() in TT._member_names_) and (TT[self.token.val.upper()].value in range(301, 320))):
            self.__matchToken(TT.KEYWD)
            ident = self.token.val
            self.__matchToken(TT.IDENT)
            self.__matchToken(TT.EQ)
            result = self.__expr()
            if result == None:
                return
            else:
                self.symTable[ident] = result
        else:
            self.__error(
                err.syntaxErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size,
                f"Expected identifier type (KEYWD), got {self.token.val} ({self.token.typ.name}) at line {self.lexer.line} pos {self.lexer.printPos-self.token.size}."
            )
            if self.__checkToken(TT.IDENT):
                self.__readToken()
                if self.__checkToken(TT.EQ):
                    self.__readToken()
                    result = self.__expr()
                    if result == None:
                        self.__error(err.exprErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size)
                else:
                    self.__error(err.syntaxErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size,
                                 f"Expected '=' (EQ), got {self.token.val} ({self.token.typ.name}) on line {self.lexer.line} pos {self.lexer.printPos-self.token.size}.")
            else:
                self.__error(err.syntaxErr, self.token, self.lexer.line, self.lexer.printPos,
                             f"Expected IDENT, got {self.token.val} ({self.token.typ.name}) on line {self.lexer.line} pos {self.lexer.printPos-self.token.size}.")
    
    def __fun(self):
        print("KEYWD: fun")
        self.__matchToken(TT.KEYWD, "fun")
        funcName = self.token.val
        self.__matchToken(TT.IDENT)
        self.__matchToken(TT.LPAREN)
        parameters:ty.Dict[str, str]|str = self.__parameters(funcName)
        self.__matchToken(TT.RPAREN)

        if parameters != "inv":
            self.funcTable[funcName] = parameters

        self.__matchToken(TT.LFLOBRAC)
        while not self.__checkToken(TT.RFLOBRAC):
            self.__statement()
        
        self.__matchToken(TT.RFLOBRAC)
    
    def __comp(self):
        print("COMPARISON")
        lparen:bool = False

        if self.__checkToken(TT.LPAREN):
            lparen = True
            self.__readToken()
        
        result:int|float|None = self.__expr()
        invalid:bool = False

        if result == None:
            invalid = True

        if self.isComparisonOp(self.token):
            comp = self.token.val
            self.__readToken()
            result2:int|float|None = self.__expr()

            if lparen:
                self.__matchToken(TT.RPAREN)

            if result2 == None:
                return
            if not invalid:
                return ops[comp](result, result2)
            return
        
        else:
            self.__error(
                err.syntaxErr, self.token, self.lexer.line, self.lexer.printPos,
                msg=f"Expected comparison operator at line {self.lexer.line} pos {self.lexer.printPos-self.token.size}."
            )

    def __expr(self):
        print("EXPRESSION")
        result:int|float|bool|None = self.__term()
        invalid:bool = False

        while (temp:=self.__checkToken(TT.PLUS)) or self.__checkToken(TT.MINUS):
            self.__readToken()
            result = ops["+=" if temp else "-="](result, self.__term())
        
        if result in (inf, nan):
            invalid = True
        
        if self.isComparisonOp(self.token):
            comp = self.token.val
            self.__readToken()
            result2 = self.__expr()
            if result2 == None:
                return
            result = ops[comp](result, result2)
        
        if invalid:
            return
        return result
    
    def __term(self):
        result:int|float = self.__unary()
        invalid:bool = False
        invalidNone:bool = False

        if result in (inf, nan):
            invalid = True
        
        if result == None:
            invalidNone = True

        while (temp:=self.__checkToken(TT.ASTERISK)) or self.__checkToken(TT.FSLASH):
            self.__readToken()
            result2 = self.__unary()
            if not invalidNone:
                result = ops["*=" if temp else "/="](result, result2)
            else:
                return nan
        
        if invalid:
            return nan
        return result
    
    def __unary(self):
        prevSym:str = ''

        if (self.__checkToken(TT.MINUS)) or self.__checkToken(TT.PLUS):
            prevSym = self.token.val
            prevSymLine, prevSymPos = self.lexer.line, self.lexer.printPos
            self.__readToken()
        
        result:int|float
        if ot.isInt(str(result:=self.__primary())):
            result = int(prevSym + str(result))
        elif result in (True, False):
            return bool(str(prevSym) + str(result))
        else:
            result = float(prevSym + str(result))
        
        return result
    
    def __primary(self):
        result:int|float

        if (temp:=self.__checkToken(TT.INT)) or self.__checkToken(TT.FLOAT):
            result = int(self.token.val.val) if temp else float(self.token.val.val)
            self.__readToken()
            return result
        
        elif self.__checkToken(TT.IDENT):
            if result:=self.symTable.get(self.token.val):
                self.__readToken()
                return result
            else:
                self.__error(err.unknownIdent, self.token, self.lexer.line, self.lexer.printPos-self.token.size)
                return inf
        
        elif self.__checkToken(TT.LPAREN):
            invalid:bool = False
            self.__readToken()
            result = self.__expr()
            if result == None:
                invalid = True
            self.__matchToken(TT.RPAREN)

            if invalid:
                return inf
            return result
        
        else:
            return inf

    def __iter(self):
        arr:ty.Any = []
        if self.token.typ == TT.LSQBRAC:
            self.__matchToken(TT.LSQBRAC)


    def __parameters(self, function:str) -> ty.Dict[str, str]|str:
        print("PARAMETERS")
        paras:ty.Dict[str, str] = {}
        
        while (self.token.typ == TT.KEYWD and TT[self.token.val.upper()].value in range(301, 340)):
            typ:TT = TT[self.token.val.upper()]
            self.__matchToken(TT.KEYWD)
            ident:str = self.token.val
            self.__matchToken(TT.IDENT)
            paras[ident] = typ.name
            
            if self.__checkToken(TT.COMMA):
                self.__readToken()
        
        if not self.__checkToken(TT.RPAREN):
            self.__error(err.invalidParametersErr, self.token, self.lexer.line, self.lexer.printPos-self.token.size, function)
            return "inv"
        
        return paras

    def isComparisonOp(self, token:tok.Token):
        return token.typ in (TT.LT, TT.LTEQ, TT.GT, TT.GTEQ, TT.EQEQ, TT.NOTEQ)
