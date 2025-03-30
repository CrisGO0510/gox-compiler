from lexer import tokenize
from rich import print
from parser import RecursiveDescentParser
from serialize import save_to_json_file, to_json

text = """
const PI float = 3.1415;
var radius int = 10;

 func main(a float, b float) float {
     var x float = 5;
     var y float = 10;
     var z float;
     }

func main() int{
    var result float;
    if radius > 0 {
        result = area(radius);
        print result;
    } else {
        print -1;
    }

    while result > 50 {
        result = result - 1;
        if result == 55 {
            break;
        }
    }

    continue;
    print 1;
}

"""

tokens = list(tokenize(text))
indexToken = 0

print(tokens)

AST = RecursiveDescentParser(tokens, indexToken).program()

print(AST)

print(to_json(AST))
save_to_json_file(AST, "ast_output.json")
