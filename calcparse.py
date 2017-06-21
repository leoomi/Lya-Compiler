from lyaparser import *
from codeGen import *

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    #visit = visitor.visit(result)
    
    print("--START--")
    vis(result)
    print(code)
    for i in refs:
        print(i, refs[i])


