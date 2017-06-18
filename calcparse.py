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
    #visit recursively (DFS)
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

    
    if isinstance(node, Program):
        code.append(('end',))

    elif isinstance(node, Declaration):
        if isinstance(node.mode, DiscreteMode):
            varSize = 1
        else:
            #GET ARRAY AND STRING LEN
            varSize = 1

        code.append(('acl', varSize * len(node.identifier_list)))

        #add reference to stack
        for i in node.identifier_list:
            refs[i.label] = sp
            sp += 1
        
        if isinstance(node.initialization, Constant):
            for i in node.identifier_list:
                code.append(('ldc', node.initialization.value))
                code.append(('stv','ALTERAR',refs[i.label]))

    elif isinstance(node, BuiltinCall):
        if node.builtin_name == "read":
            for i in node.parameter_list:
                #CHECK IF TYPE IS INT
                if True:
                    code.append(('rdv',))
                    code.append(('stv','ALTERAR',refs[i.label]))
                #CHECK IF TYPE IS STRING
                else:
                    code.append(('ldr', 'ALTERAR', 'ALTERAR'))
                    code.append(('rds',))
        elif node.builtin_name == "print":
            for i in node.parameter_list:
                #CHECK IF TYPE IS INT
                if True:
                    code.append(('prv', 0))
                else:
                    code.append(('prv', 1))
    
    elif isinstance(node, BinaryOperation) or isinstance(node, RelationalOperation):
        if hasattr(node.left, "label"):
            code.append(('ldv','ALTERAR',refs[node.left.label]))
        elif hasattr(node.left, "value"):
            code.append(('ldc', node.left.value))
        if hasattr(node.right, "label"):
            code.append(('ldv','ALTERAR',refs[node.right.label]))
        elif hasattr(node.right, "value"):
            code.append(('ldc', node.right.value))

        if node.operator == "*":
            code.append(('mul',))
        elif node.operator == "+":
            code.append(('add',))
        elif node.operator == "-":
            code.append(('sub',))
        elif node.operator == "/":
            code.append(('div',))
        elif node.operator == "%":
            code.append(('mod',))
        elif node.operator == "&&":
            code.append(('and',))
        elif node.operator == "||":
            code.append(('lor',))
        elif node.operator == "<":
            code.append(('les',))
        elif node.operator == "<=":
            code.append(('leq',))
        elif node.operator == ">":
            code.append(('grt',))
        elif node.operator == ">=":
            code.append(('gre',))
        elif node.operator == "==":
            code.append(('equ',))
        elif node.operator == "!=":
            code.append(('neq',))
    
    elif isinstance(node, UnaryOperation):
        if hasattr(node.operand, "label"):
            code.append(('ldv','ALTERAR',refs[node.operand.label]))
        elif hasattr(node.operand, "value"):
            code.append(('ldc', node.operand.value))

        if node.operator == "!":
            code.append(("not",))
        if node.operator == "-":
            code.append(("neg",))

while True:
    try:
        s = input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    #visit = visitor.visit(result)
    
    print("--START--")
    code.append(('stp',))
    vis(result)
    print(code)
    for i in refs:
        print(i, refs[i])


