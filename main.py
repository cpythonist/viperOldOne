# log:bool = False

# try:
#     import logging as lg
#     handler:lg.FileHandler = lg.FileHandler(filename="logs\\mainErr.log", mode="a")
#     handler.setLevel(lg.DEBUG)
#     handler.setFormatter(lg.Formatter("\n%(asctime)s\n%(levelname)s: %(name)s: %(message)s"))
#     logger = lg.getLogger("main")
#     logger.addHandler(handler)
#     log = True

# except (ModuleNotFoundError, FileNotFoundError) as e:
#     print(e.__class__.__name__, e)
#     print("Logger not found. Program will continue without logging.")

# except Exception as e:
#     print("Unknown error while trying to initialise logger.")

# try:
import sys
import traceback

sys.path.insert(1, ".\\core")
import core.lex as clex
import core.parse as cparse
with open("tests\\main.vi", 'r') as f:
    code:str = f.read()

lexer:clex.Lexer = clex.Lexer(code)
parser:cparse.Parser = cparse.Parser(lexer)

parser.parse()

# except (ModuleNotFoundError, FileNotFoundError):
#     import traceback
#     traceback.print_exc()
#     print("Critical files not found.")

# except Exception as e:
#     if log:
#         logger.fatal(f"Fatal error:\n{traceback.format_exc()}")
#     else:
#         print(f"Logging unavailable, error will be printed with output:\nFatal error:\n{traceback.format_exc()}")
