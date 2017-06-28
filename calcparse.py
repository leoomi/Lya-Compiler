from lyaparser import *
from codeGen import *
from lyavm import *

try:
    s = input('calc > ')
except EOFError:
    exit()

result = parser.parse(s)
visit = visitor.visit(result)

#generate the code
codeGen(result)
print(code)
#run the code
vm = LyaVM();
vm.interpret(code, H)

