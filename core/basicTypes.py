import typing as ty

class VInt:
    def __init__(self, val:int) -> None:
        self.val:int = int(val)
    
    def __repr__(self) -> str:
        return f"int({self.val})"


class VFloat:
    def __init__(self, val:float) -> None:
        self.val:float = float(val)
    
    def __repr__(self) -> str:
        return f"float({self.val})"


class VString:
    def __init__(self, val:str) -> None:
        self.val:str = str(val)
    
    def __repr__(self) -> str:
        return f"string({self.val})"
    
    def join(self, iter:ty.List[ty.Self]|ty.Tuple[ty.Self]|ty.Set[ty.Self]|ty.Dict[ty.Self, ty.Any]) -> str:
        result = self.val
        for i in iter:
            if isinstance(i, ty.Self):
                result += i.val
        return result
    
    def length(self) -> int:
        return len(self.val)


class VBool:
    def __init__(self, val:str) -> None:
        self.val = bool(val)
    
    def __str__(self) -> str:
        return f"bool({self.val})"


class VIdent:
    def __init__(self, name:str, val:ty.Any) -> None:
        self.name:str = name
        self.val:ty.Any = val
    
    def __str__(self) -> str:
        return f"ident({self.name}:{self.val})"