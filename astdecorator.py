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
    def __init__(self, kind, operators, default) 
        self.type = kind
        self.operators = operators
        self.default = default


int_type = ExprType("int", ["+","-","*","/","%",">",">=","<","<="], 0)
bool_type = ExprType("bool", ["&&","||","!"], True)
char_type = ExprType("char", ["&","==","!="], "")
string_type = ExprType("string", ["&","==","!="], "")

class Environment(object):
    def __init__(self):
        self.stack = []
        self.root = SymbolTable()
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
