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

class Program(AST):
    _fields = [’stmts’]
    
#atribuir valor para atributo _typo através de um construtor antes do super construtor?
#dessa forma consigo aplicar a "lógica" para obter tipo resultante, caso contrário, de que forma seria?

class If_Action(AST):
    _fields = []
    def __init__(self,*args,**kwargs):
        _type #TO BE CONTINUED
