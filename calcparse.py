from lyaparser import *

#reference of nodes to stack
refs = {}
#stack pointer
sp = 0
#index for display
d = 0
#generated code
code = []

def vis(node):
    global refs, sp, code
    print(node)
    if isinstance(node, Program):
        code.append(('stp',))

    elif isinstance(node, Declaration):
        if isinstance(node.mode, DiscreteMode):
            varSize = 1
        else:
            #GET ARRAY AND STRING LEN
            varSize = 1
        code.append(('acl', varSize * len(node.identifier_list)))

        #add reference to stack
        for i in node.identifier_list:
            refs[i] = sp
            sp += 1
        
        if isinstance(node.initialization, Constant):
            #se tiver inicializacao fazer LDC + STR


    #visit recursively
    if hasattr(node,"_fields"):
        for field in getattr(node,"_fields"):
            print (field)
            val = getattr(node,field,None)            
            if (isinstance(val,list)):
                for v in val:
                    vis(v)
            else:
                vis(val)
        print("Returning...")
    else:
        print("Leaf node...")


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
    print(refs)


