import pdb
import copy

class SymbolTable(dict):
    """
        Class representing a symbol table. It should
        provide functionality for adding and looking
        up nodes associated with identifiers.
    """
    def __init__(self, decl=None):
        super().__init__()
        self.decl = decl
    def add(self, name, value):
        self[name] = value
    def lookup(self, name):
        return self.get(name, None)
    def return_type(self):
        if self.decl:
            return self.decl.mode
        return None

class ExprType(object):
    def __init__(self, kind, operators, default):
        self.type = kind
        self.operators = operators
        self.default = default
        
class FunctionArgs():
    def __init__(self, args):
        self.args = args

int_type = ExprType("int", ["+","-","*","/","%",">",">=","<","<=", "!=", "=="], 0)
bool_type = ExprType("bool", ["&&","||","!"], True)
char_type = ExprType("char", ["&","==","!="], "")
string_type = ExprType("string", ["&","==","!="], "")

expr_type_list = {'int': int_type, 'bool': bool_type, 'char': char_type, 'string': string_type}

class Environment(object):
    def __init__(self):
        self.stack = []
        self.root = SymbolTable()
        self.functions = {}
        self.stack.append(self.root)
        self.root.update({
            "int": int_type,
            "char": char_type,
            "string": string_type,
            "bool": bool_type
        })
    def push(self, enclosure):
        self.stack.append(SymbolTable(decl=enclosure))
    def pop(self):
        self.stack.pop()
    def peek(self):
        return self.stack[-1]
    def scope_level(self):
        return len(self.stack)
    def add_local(self, name, value):
        self.peek().add(name, value)
    def add_root(self, name, value):
        self.root.add(name, value)
    def lookup(self, name):
        for scope in reversed(self.stack):
            hit = scope.lookup(name)
            if hit is not None:
                return hit
        return None
    def find(self, name):
        if name in self.stack[-1]:
            return True
        else:
            return False

class AST(object):
    """
        Base class example for the AST nodes.  Each node is expected to
        define the _fields attribute which lists the names of stored
        attributes.   The __init__() method below takes positional
        arguments and assigns them to the appropriate fields.  Any
        additional arguments specified as keywords are also assigned.
    """
    _fields = []
    def __init__(self,*args,**kwargs):
        assert len(args) == len(self._fields)
        for name,value in zip(self._fields,args):
            setattr(self,name,value)
            # Assign additional keyword arguments if supplied
            for name,value in kwargs.items():
                setattr(self,name,value)

class NodeVisitor(object):
    """
    Class for visiting nodes of the parse tree.  This is modeled after
    a similar class in the standard library ast.NodeVisitor.  For each
    node, the visit(node) method calls a method visit_NodeName(node)
    which should be implemented in subclasses.  The generic_visit() method
    is called for all nodes where there is no matching visit_NodeName()
    method.
    Here is a example of a visitor that examines binary operators:
    class VisitOps(NodeVisitor):
        visit_Binop(self,node):
            print("Binary operator", node.op)
            self.visit(node.left)
            self.visit(node.right)
        visit_Unaryop(self,node):
            print("Unary operator", node.op)
            self.visit(node.expr)
    tree = parse(txt)
    VisitOps().visit(tree)
    """

    def visit_Program(self, node):
        self.environment.push(node)
        node.environment = self.environment
        node.symtab = self.environment.peek()

        for stmt in node.stmts:
            self.visit(stmt)
    
    def visit_Constant(self, node):
        print(node)
        print("Constant: ", node.type)
        print("Constant: ", node.value)

    def visit_Identifier(self, node):
        print("Identifier: ", node.label)
        if(self.environment.lookup(node.label) == None):
            print("Variable not declared: ", node.label)
            exit()
        else:
            node.type = self.environment.lookup(node.label)

    def visit_Declaration(self, node):
        print(node)
        print("Declaration: ", node.identifier_list)
        self.visit(node.mode)
        self.visit(node.initialization)

        init = None
        error = False
        if(node.initialization != None):
            if(node.initialization.type == node.mode.type):
                init = expr_type_list[node.initialization.type].default
            else:
                print("Conflicting types in declaration: ", node.initialization.type, node.mode.type)
                error = True
                exit()

        if(not error):
            for i in node.identifier_list:
                if(self.environment.peek().lookup(i.label) == None):
                    if(node.mode.__class__.__name__ == 'ArrayMode'):
                        pdb.set_trace()
                        self.environment.peek().add(i.label, '[' + node.mode.element_mode.type + ']')
                    elif(node.mode.type.__class__.__name__ == 'ExprType'):
                        self.environment.peek().add(i.label, node.mode.type.type)
                    else:
                        self.environment.peek().add(i.label, node.mode.type)
                else:
                    print("Multiply defined variable: ", i.label)
                    exit()

    def visit_SynonymDefinition(self, node):
        print("Synonym: ", node.identifier_list)
        self.visit(node.mode)
        self.visit(node.initialization)

        init = None
        error = False
        if(node.initialization != None):
            if(node.initialization.type == node.mode.type):
                init = expr_type_list[node.initialization.type].default
            else:
                print("Conflicting types in synonym: ", node.initialization, node.mode.type)
                exit()
                error = True

        if(not error):
            for i in node.identifier_list:
                if(self.environment.peek().lookup(i.label) == None):
                    self.environment.peek().add(i.label, node.mode.type)
                else:
                    print("Multiply defined variable: ", i.label)
                    exit()
        
                    
    def visit_AssignmentAction(self, node):
        print("Assignment")
        self.visit(node.location)
        self.visit(node.expression)
        #pdb.set_trace()
        label = None
        #get leftside label
        if(node.location.__class__.__name__ == 'Element'):
            label = node.location.label.label
        elif(hasattr(node.location,'label')):
            label = node.location.label
        elif(hasattr(node.location.id,'label')):
            label = node.location.id.label
        #builtin call
        else:
            label = node.location.builtin_name
        
        exp = None
        if(node.expression.__class__.__name__ == 'Element'):
            exp = self.environment.lookup(node.expression.label.label)
        elif(node.expression.type != None):
            exp = node.expression.type
        else:
            exp = self.environment.lookup(node.expression.label)

        if(self.environment.lookup(label).__class__.__name__ == 'ExprType'):
            location = self.environment.lookup(label).type
        else:
            location = self.environment.lookup(label)

        if(exp.__class__.__name__ == 'ExprType'):
            exp = exp.type
            
        #check if label and expression share same type
        if(location != exp):
            print("Conflicting types for assignment action: ", label, location, exp)
            exit()
        else:
            if(node.assigning_operator.closed_dyadic_operator != None):
                expr_type = None
                for key, i in expr_type_list.items():
                    if(node.assigning_operator.closed_dyadic_operator in i.operators):
                        expr_type = i
            
                if(expr_type != None):
                    if(expr_type.type != location or expr_type.type != exp):
                        print("Conflicting types for assignment action: ", label, location, expr_type.type, exp)
                        exit()
           
    def visit_UnaryOperation(self, node):
        self.visit(node.operand)
        print(node)
        exp = None
        if(node.operand.type != None):
            exp = node.operand.type
        else:
            exp = self.environment.lookup(node.operand.label)
        
        expr_type = None
        for key, i in expr_type_list.items():
            if(node.operator in i.operators):
                expr_type = i

        if (expr_type.type != exp):
            print("Conflicting type for Unary Operation: ", exp, expr_type.type)
            exit()
        
        node.type = expr_type.type;

    def visit_DiscreteMode(self, node):
        print(node)
        print("Discrete Mode: ",node.type)

    def visit_ProcedureCall(self, node):
        print('Procedure Call:', node.id.label)
        if(self.environment.lookup(node.id.label) == None):
            print("Function not declared: ", node.id.label)
            exit()
            
        argList = []
 
        for param in node.parameter_list:
            if param.__class__.__name__ == 'Identifier':
                print('ProcCall param: ', self.environment.lookup(param.label))
                argList.append(self.environment.lookup(param.label))
            else:
                print('ProcCall param: ')
                self.visit(param)
                argList.append(param.type)
            
        if not len(node.parameter_list) == len(self.environment.functions[(node.id.label)].args):
            print("Wrong number of arguments for function: ", node.id.label)
            exit()

        if not argList == self.environment.functions[(node.id.label)].args:
            print("conflicting types for procedure call: ", argList, ' ',self.environment.functions[(node.id.label)].args)
            exit()

        node.type = self.environment.lookup(node.id.label)
         
    def visit_BinaryOperation(self, node):
        print("Binary Op")
        self.visit(node.left)
        print("Binary Operation: ", node.operator)
        self.visit(node.right)
        
        expr_type = []
        for key, i in expr_type_list.items():
            if(node.operator in i.operators):
                expr_type.append(i)
        #get exp type
        exp = None
        exp2 = None

        if(hasattr(node.left, 'type')):
            if(node.left.type != None):
                exp = node.left.type
            else:
                exp = self.environment.lookup(node.left.label)
        elif(node.left.__class__.__name__ == 'Element'):
            exp = self.environment.lookup(node.left.label.label)
        '''else:
            if(node.left.__class__ == 'ProcedureCall'):
                exp = self.environment.lookup(node.left.id)'''
        
        if(hasattr(node.right, 'type')):
            if(node.right.type != None):
                exp2 = node.right.type
            else:
                exp2 = self.environment.lookup(node.right.label)

        if(expr_type != None):
            found = False
            print(exp, exp2)
            for i in expr_type:
                if(i.type == exp or i.type == exp2):
                    found = True
                    node.type = i.type
                    break
                
            if not found:
                print("Conflicting types in binary operation: ", exp, node.operator, exp2)
                exit()
    
    def visit_IfAction(self, node):
        self.visit(node.boolean_expression)
        
        self.environment.push(None)
        self.visit(node.then_clause) 
        self.environment.pop()
        
        if (node.else_clause != None):
            self.environment.push(None)
            self.visit(node.else_clause)
            self.environment.pop()

    #Check return type
    #Add label id to symbol table
    #Create Scope for procedure_definition
    def visit_ProcedureStatement(self, node):
        print("ProcedureStatement: ", node.label_id.label)
        type = "Void" if node.procedure_definition.result_spec == None else node.procedure_definition.result_spec.mode.type
        self.environment.add_root(node.label_id.label, type)
        self.lastProcAdded = node.label_id.label
        self.visit(node.label_id)
        self.environment.push(node.label_id.label)
        self.visit(node.procedure_definition)
        self.environment.pop()

    def visit_ProcedureDefinition(self, node):
        args = []

        if node.formal_parameter_list != None:
            for param in node.formal_parameter_list:
                for identifier in param.identifier_list:
                    if(self.environment.peek().lookup(identifier.label) == None):
                        if param.parameter_spec.mode.type != None:
                            mode = param.parameter_spec.mode.type
                        else:
                            mode = expr_type_list[param.parameter_spec.mode.label].type
                        self.environment.peek().add(identifier.label, mode)
                        args.append(mode)
                    else:
                        print("Multiply defined variable: ", identifier.label)
                        exit()

        self.environment.functions[self.lastProcAdded] = FunctionArgs(args)
        
        if node.statement_list != None:
            for statement in node.statement_list:
                if hasattr(statement, 'action'):
                    if statement.action.__class__.__name__ == "ReturnAction":
                        exp = None
                        if(statement.action.value.type != None):
                            exp = statement.action.value.type
                        else:
                            exp = self.environment.lookup(statement.action.value.label)

                        func = self.environment.lookup(self.environment.peek().decl)

                        print(exp, func)
                        if(exp != func):
                            print("Conflicting return type: ", exp, func)
                            exit()

                self.visit(statement)

    def visit_ConditionalExpression(self, node):
        self.visit(node.boolean_expression)
        self.visit(node.then_expression)
        thenType = node.then_expression.type
        if(node.elsif_expression != None):
            self.visit(node.elsif_expression)
            elsifType = node.elsif_expression.type
        else:
            elsifType = thenType
        self.visit(node.else_expression)
        elseType = node.else_expression.type

        if (thenType != elsifType or thenType != elseType or elsifType != elseType):
            print("Conflicting types in conditional expression (ternaryop): ", thenType, elsifType, elseType)
            exit()
        else:
            node.type = thenType

    def visit_NewmodeStatement(self, node):
        print("Newmode statement:")

        for i in node.newmode_list:
            self.visit(i)

    def visit_ModeDefinition(self, node):
        for i in node.identifier_list:
            if i.label not in expr_type_list:
                if (node.mode.__class__.__name__ == 'ArrayMode'):
                    modeLabel = node.mode.element_mode.type
                    mode = copy.deepcopy(expr_type_list[modeLabel])
                    mode.type = '[' + mode.type + ']'
                else:
                    modeLabel = node.mode.label.type
                    mode = expr_type_list[modeLabel]
                self.environment.add_root(i.label, mode)
                expr_type_list[i.label] = mode
            else:
                print('mode name already declared: ', i.label)
                exit()
        
    def visit(self,node):
        """
        Execute a method of the form visit_NodeName(node) where
        NodeName is the name of the class of a particular node.
        """

        if node:
            method = 'visit_' + node.__class__.__name__
            visitor = getattr(self, method, self.generic_visit)
            return visitor(node)
        else:
            return None

    def generic_visit(self,node):
        """
        Method executed if no applicable visit_ method can be found.
        This examines the node to see if it has _fields, is a list,
        or can be further traversed.
        """
        print(node)
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list) or isinstance(value,tuple):
                for item in value:
                    if isinstance(item,AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)
        
    def __init__(self):
        self.environment = Environment()

class Program(AST):
    _fields = ['stmts']

class Statement(AST):
    _fields = ['sort']

class DeclarationStatement(AST):
    _fields = ['dcl_list']
    
class Declaration(AST):
    _fields = ['identifier_list', 'mode', 'initialization']

class SynonymStatement(AST):
    _fields = ['syn_list']
    
class SynonymDefinition(AST):
    _fields = ['identifier_list', 'mode', 'initialization']

class NewmodeStatement(AST):
    _fields = ['newmode_list']
    
class ModeDefinition(AST):
    _fields = ['identifier_list', 'mode']

class DiscreteMode(AST):
    _fields = ['type']

class RangeMode(AST):
    _fields = ['discrete_mode', 'literal_range']

class LiteralRange(AST):
    _fields = ['lower_bound', 'upper_bound']

class StringMode(AST):
    _fields = ['string_length', 'type']

class ArrayMode(AST):
    _fields = ['index_mode_list', 'element_mode']

class Element(AST):
    _fields = ['label', 'start_element']

class Slice(AST):
    _fields = ['label', 'left_element', 'right_element']

class StringElement(AST):
    _fields = ['string_location', 'start_element']

class StringSlice(AST):
    _fields = ['string_location', 'left_element', 'right_element']

class ArrayElement(AST):
    _fields = ['array_location', 'expression_list']

class ArraySlice(AST):
    _fields = ['array_location', 'lower_bound', 'upper_bound']
    
class Add(AST):
    _fields = ['left', 'right']

class And(AST):
    _fields = ['nodes']

class Assign(AST):
    _fields = ['nodes', 'expr']

class Variable(AST):
    _fields = ['name', 'value', 'type', 'lineno']

class Constant(AST):
    _fields = ['type', 'value']

class ValueArrayElement(AST):
    _fields = ['array_primitive_value', 'expression_list']

class ValueArraySlice(AST):
    _fields = ['array_primitive_value', 'lower_bound', 'upper_bound']

class ConditionalExpression(AST):
    _fields = ['boolean_expression', 'then_expression', 'elsif_expression', 'else_expression', 'type']

class ElsifExpression(AST):
    _fields = ['elsif_expression', 'boolean_expression', 'then_expression']

class BinaryOperation(AST):
    _fields = ['left', 'operator', 'right', 'type']

class UnaryOperation(AST):
    _fields = ['operator','operand', 'type']

class Identifier(AST):
    _fields = ['label', 'type']

class Operand0(AST):
    _fields = ['operand0', 'operator1', 'operand1']

class Operand1(AST):
    _fields = ['operand1', 'operator2', 'operand2']

class Operand2(AST):
    _fields = ['operand2', 'arithmetic_mult_op', 'operand3']

class Operand3(AST):
    _fields = ['monadic_operator', 'operand4']

class ActionStatement(AST):
    _fields = ['label_id', 'action']

class DoAction(AST):
    _fields = ['control_part', 'many_action_statement']

class ControlPart(AST):
    _fields = ['control', 'while_control']

class StepEnumeration(AST):
    _fields = ['loop_counter', 'assignment_symbol', 'start_value', 'step_value','down', 'end_value']

class AssignmentAction(AST):
    _fields = ['location', 'assigning_operator', 'expression']

class AssigningOperator(AST):
    _fields = ['closed_dyadic_operator', 'assignment_symbol']

class IfAction(AST):
    _fields = ['boolean_expression', 'then_clause', 'else_clause']

class ThenClause(AST):
    _fields = ['many_action_statement']

class ElseClause(AST):
    _fields = ['many_action_statement', 'boolean_expression', 'then_clause', 'else_clause']

class RangeEnumeration(AST):
    _fields = ['loop_counter', 'down', 'discrete_mode']

class ProcedureCall(AST):
    _fields = ['id','parameter_list']

class BuiltinCall(AST):
    _fields = ['builtin_name', 'parameter_list']

class ProcedureStatement(AST):
    _fields = ['label_id', 'procedure_definition']

class ProcedureDefinition(AST):
    _fields = ['formal_parameter_list', 'result_spec', 'statement_list']

class FormalParameter(AST):
    _fields = ['identifier_list', 'parameter_spec']
    
class ParameterSpec(AST):
    _fields = ['mode', 'parameter_attribute']
    
class ResultSpec(AST):
    _fields = ['mode', 'result_attribute']

class ReturnAction(AST):
    _fields = ['value']
