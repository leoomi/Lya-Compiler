from lyaparser import *

#reference of nodes to stack
refs = [{}]
#stack pointer
sp = [0]
#index for display
dCount = 1
d = [0]
#stack for labels
labels = []
labelN = 0
#generated code
code = []
#allocated mem
mem = [0]
#string constants
H = []

def codeGen(node):
    global refs, sp, dCount, d, code, labels, labelN, mem, H
    
    if isinstance(node, Program):
        code.append(('stp',))

    elif isinstance(node, ProcedureStatement):
        #Jump to end of procedure definition
        code.append(('jmp', labelN))
        labels.append(labelN)
        labelN += 1
        #Label to beginning of the procedure
        code.append(('lbl', labelN))
        refs[d[0]][node.label_id.label] = labelN
        labelN += 1

        code.append(('enf', dCount))
        refs.append({})
        mem.append(0)
        sp.append(0)
        d.append(dCount)
        dCount += 1

    elif isinstance(node, ProcedureDefinition):
        count = -3
        if node.formal_parameter_list != None:
            for i in node.formal_parameter_list:
                for j in i.identifier_list:
                    refs[-1][j.label] = count
                    count -= 1

        refs[-1]["ret"] = count


    elif isinstance(node, IfAction):
        codeGen(node.boolean_expression)
        #jump to end of then actions
        code.append(('jof', labelN))
        labels.append(labelN)
        labelN += 1
        
        codeGen(node.then_clause)
        if node.else_clause != None:
            #jump to end of else clause after then clause
            code.append(('jmp', labelN))
            #label to then clause
            code.append(('lbl', labels.pop()))
            labels.append(labelN)
            labelN += 1
            
            codeGen(node.else_clause)
            #label to else clause
            code.append(('lbl', labels.pop()))
        else:
            #label to then clause
            code.append(('lbl', labels.pop()))
        #Did all visiting already, no need to visit recursively again    
        return

    elif isinstance(node, DoAction):
        #label to while condition
        code.append(('lbl', labelN))
        labels.append(labelN)
        labelN += 1
        
        codeGen(node.control_part)
        
        #Jump to end of while
        code.append(('jof', labelN))
        labels.append(labelN)
        labelN += 1
        if node.many_action_statement != None:
            for v in node.many_action_statement:
                codeGen(v)
        
        #jump to while condition
        code.append(('jmp', labels[-2]))
        code.append(('lbl', labels.pop()))
        labels.pop()
        #Did all visiting already, no need to visit recursively again    
        return

    #print(node)
    #visit recursively (DFS)
    if hasattr(node,"_fields"):
        for field in getattr(node,"_fields"):
            #print (field)
            val = getattr(node,field,None)            
            if (isinstance(val,list)):
                for v in val:
                    codeGen(v)
            else:
                codeGen(val)
        #print("Returning...")
    #else:
        #print("Leaf node...")

    
    if isinstance(node, Program):
        code.append(('dlc', mem.pop()))
        code.append(('end',))

    elif isinstance(node, Declaration):
        if isinstance(node.mode, DiscreteMode):
            varSize = 1
        elif isinstance(node.mode, StringMode):
            varSize = node.mode.string_length.value + 1
        #elif isinstance(node.mode, ArrayMode): 
        #CHECK SIZE FOR ARRAYMODE
            

        code.append(('alc', varSize * len(node.identifier_list)))
        mem[-1] += varSize * len(node.identifier_list)
        

        #add reference to stack
        for i in node.identifier_list:
            refs[d[-1]][i.label] = sp[-1]
            sp[-1] += varSize
        
        if isinstance(node.initialization, Constant):
            for i in node.identifier_list:
                code.append(('ldc', node.initialization.value))
                code.append(('stv', d[-1], refs[d[-1]][i.label]))

    elif isinstance(node, BuiltinCall):
        if node.builtin_name == "read":
            for i in node.parameter_list:
                #CHECK IF TYPE IS INT
                if True:
                    code.append(('rdv',))
                    code.append(('stv', d[-1], refs[d[-1]][i.label]))
                #CHECK IF TYPE IS STRING
                else:
                    code.append(('ldr', 'ALTERAR', 'ALTERAR'))
                    code.append(('rds',))
        elif node.builtin_name == "print":
            for i in node.parameter_list:
                if isinstance(i, Constant):
                    if i.type == "string":
                        code.append(('prc',len(H)))
                        H.append(i.value)
                    else:
                        code.append(('ldc', i.value))
                        code.append(('prv', 0))
                #Check variables types
                elif isinstance(i, Identifier):
                    code.append(('ldv', d[-1], refs[d[-1]][i.label]))
                    code.append(('prv', 0))
                else:
                    code.append(('prv', 0))
                
                sp[-1] -= 1
    
    elif isinstance(node, BinaryOperation):
        if hasattr(node.left, "label"):
            code.append(('ldv', d[-1], refs[d[-1]][node.left.label]))
            sp[-1]+=1
        elif hasattr(node.left, "value"):
            code.append(('ldc', node.left.value))
            sp[-1]+=1
        if hasattr(node.right, "label"):
            code.append(('ldv', d[-1], refs[d[-1]][node.right.label]))
            sp[-1]+=1
        elif hasattr(node.right, "value"):
            code.append(('ldc', node.right.value))
            sp[-1]+=1

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
        sp[-1]-=1

    elif isinstance(node, UnaryOperation):
        if hasattr(node.operand, "label"):
            code.append(('ldv', d[-1], refs[d[-1]][node.operand.label]))
            sp[-1]+=1
        elif hasattr(node.operand, "value"):
            code.append(('ldc', node.operand.value))
            sp[-1]+=1

        if node.operator == "!":
            code.append(("not",))
        if node.operator == "-":
            code.append(("neg",))
    
    elif isinstance(node, AssignmentAction):
        if node.assigning_operator.closed_dyadic_operator != None:
            code.append(('ldv', d[-1], refs[d[-1]][node.location.label]))

        if hasattr(node.expression, "value"):
            code.append(('ldc', node.expression.value))
            sp[-1]+=1

        if node.assigning_operator.closed_dyadic_operator == '*':
            code.append(('mul',))
        elif node.assigning_operator.closed_dyadic_operator == '+':
            code.append(('add',))
        elif node.assigning_operator.closed_dyadic_operator == '-':
            code.append(('sub',))
        elif node.assigning_operator.closed_dyadic_operator == '/':
            code.append(('div',))
        elif node.assigning_operator.closed_dyadic_operator == '%':
            code.append(('mod',))
        #elif node.assigning_operator.closed_dyadic_operator == '&':
        
        
        if hasattr(node.location, "label"):
            code.append(('stv', d[-1], refs[d[-1]][node.location.label]))
            sp[-1]-=1
        #DO ELSE IF IT ISNT AN IDENTIFIER (ARRAY, PERHAPS?)
                    
    elif isinstance(node, ProcedureStatement):
        code.append(('dlc', mem.pop()))
        if node.procedure_definition.formal_parameter_list != None:
            count = 0
            for i in node.procedure_definition.formal_parameter_list:
                count += len(i.identifier_list)
            code.append(('ret', d.pop(), count))
        else:
            code.append(('ret', d.pop(), 0))
            
        code.append(('lbl',labels.pop()))
        sp.pop()

    elif isinstance(node, ProcedureCall):
        code.append(('alc', 1));
    
        if node.parameter_list != None:
            for i in node.parameter_list:
                code.append(('alc', 1))
                if isinstance(i, Constant):
                    code.append(('ldc', i.value))
                elif isinstance(i, Identifier):
                    code.append(('ldv', d[-1], refs[d[-1]][i.label]))
        #print(refs, mem, d)
        code.append(('cfu', refs[d[0]][node.id.label]))

    elif isinstance(node, ReturnAction):
        if isinstance(node.value, Constant):
            code.append(('ldc', node.value.value))
        code.append(('stv', d[-1], refs[d[-1]]["ret"]))
#        code.append(('dlc', sp[-1] - 2))
        code.append(('ret', d[-1], -refs[d[-1]]["ret"]-3))
    
