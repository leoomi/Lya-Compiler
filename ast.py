
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
        

class Program(AST):
    _fields = ['stmts']

class Statement(AST):
    _fields = ['type']

class Initialization(AST):
    _fields = ['expression']

class SynonymDefinition(AST):
    _fields = ['identifier_list', 'mode', 'constant_expression']

class ModeDefinition(AST):
    _fields = ['identifier_list', 'mode']

class Mode(AST):
    _fields = ['type']

class RangeMode(Mode):
    def __init__(self):
        self._fields = super._fields + ['literal_range']

class LiteralRange(AST):
    _fields = ['lower_bound', 'upper_bound']

class StringMode(Mode):
    def __init__(self):
        self._fields = super._fields + ['string_length']

class ArrayMode(Mode):
    def __init__(self):
        self._fields = super._fields + ['index_mode_list', 'element_mode']

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
    _fields = ['value', 'type']

class ValueArrayElement(AST):
    _fields = ['array_primitive_value', 'expression_list']

class ValueArraySlice(AST):
    _fields = ['array_primitive_value', 'lower_bound', 'upper_bound']

class ConditionalExpression(AST):
    _fields = ['boolean_expression', 'then_expression', 'elsif_expression', 'else_expression']

class ElsifExpression(AST):
    _fields = ['elsif_expression', 'boolean_expression', 'then_expression']

class Operand0(AST):
    _fields = ['operand0', 'operator1', 'operand1']

#Relational operator (>, <, and, or, etc) ou Membership Operator (só IN)
class RelationalOperator(AST):
    _fields = ['type' ,'value']

class Operand1(AST):
    _fields = ['operand1', 'operator2', 'operand2']

#Arithmetic additive ou string concatenation
class Operator2(AST):
    _fields = ['type', 'value']

class Operand2(AST):
    _fields = ['operand2', 'arithmetic_mult_op', 'operand3']

class Operand3(AST):
    _fields = ['monadic_operator', 'operand4']

class ActionStatement(AST):
    _fields = ['label_id', 'action']

class DoAction(AST):
    _fields = ['control_part', 'many_action_statement']

class ControlPart(AST):
    _fields = ['for_control', 'while_control']

class StepEnumeration(AST):
    _fields = ['loop_counter', 'assignment_symbol', 'start_value', 'step_value', 'end_value']

class AssignmentAction(AST):
    _fields = ['location', 'assigning_operator', 'expression']

class AssignmentOperator(AST):
    _fields = ['closed_dyadic_operator', 'assignment_symbol']

class IfAction(AST):
    _fields = ['boolean_expression', 'then_clause', 'else_clause']

class ThenClause(AST):
    _fields = ['many_action_statement']

class ElseClause(AST):
    _fields = ['many_action_statement', 'boolean_expression', 'then_clause', 'else_clause']

class RangeEnumeration(AST):
    _fields = ['loop_counter', 'discrete_mode']

class ProcedureCall(AST):
    _fields = ['parameter_list']

class ReturnAction(AST):
    _fields = ['result']

class BuiltinCall(AST):
    _fields = ['builtin_name', 'parameter_list']

class ProcedureStatement(AST):
    _fields = ['label_id', 'procedure_definition']

class ProcedureDefinition(AST):
    _fields = ['formal_paramenter_list', 'result_spec', 'statement_list']

class FormalParameter(AST):
    _fields = ['identifier_list', 'parameter_spec']
    
class ParameterSpec(AST):
    _fields = ['mode', 'parameter_attribute']
    
class ResultSpec(AST):
    _fields = ['mode', 'result_attribute']


