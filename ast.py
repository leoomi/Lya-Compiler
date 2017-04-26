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
        for field in getattr(node,"_fields"):
            value = getattr(node,field,None)
            if isinstance(value, list):
                for item in value:
                    if isinstance(item,AST):
                        self.visit(item)
            elif isinstance(value, AST):
                self.visit(value)
        
class Program(AST):
    _fields = ['stmts']
    
class Add(AST):
    _fields = ['left', 'right']

class And(AST):
    _fields = ['nodes']

class Assign(AST):
    _fields = ['nodes', 'expr']

class Variable(AST):
    _fields = ['name', 'value', 'type']

class Constant(AST):
    _fields = ['value', 'type']
