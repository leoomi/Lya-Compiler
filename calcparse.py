from lyaparser import *
from codeGen import *
from lyavm import *

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    #visit = visitor.visit(result)
   
    #generate the code
    vis(result)
    print(code)
    #run the code
    LyaVM.interpret([('stp'),('alc', 2),('rdv'),('stv', 0, 1),('ldc', 1),('stv', 0, 0),('lbl', 1),('ldv', 0, 0),('ldv', 0, 1),('leq'),('jof', 2),('ldv', 0, 0),('ldv', 0, 0),('mul'),('prv', 0),('ldv', 0, 0),('ldc', 1),('add'),('stv', 0, 0),('jmp', 1),('lbl', 2),('dlc', 2),('end')], H)

