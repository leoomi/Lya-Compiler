import os
import sys
from lyaparser import *
from codeGen import *
from lyavm import *

fpath = sys.argv[-1]

with open (fpath, "r") as myfile:
    data=myfile.read().replace('\n', '')

result = parser.parse(data)
visit = visitor.visit(result)

#generate the code
codeGen(result)
print(code)
#run the code
vm = LyaVM();
vm.interpret(code, H)

