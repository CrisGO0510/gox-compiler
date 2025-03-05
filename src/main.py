from lexer import Token, tokenize
from rich import print


tokens = list(
    tokenize(
        "const var print return break continue if else while func import true false"
    )
)

print(tokens)
