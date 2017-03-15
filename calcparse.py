# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lyalex import tokens

class Declaration:
    def __init__(self, identifier_list, mode, value=0):
        self.identifier_list = identifier_list
        self.mode = mode
        self.value = value

def p_program(p):
    'program : statement_list'
    p[0] = p[1]

def p_statement_list(p):
    '''statement_list : statement 
                      | statement_list statement'''
    if (len(p) == 2):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_statement(p):
    '''statement : declaration_statement
                 | synonym_statement
                 | newmode_statement
                 | procedure_statement
                 | action_statement'''
    p[0] = p[1]

def p_declaration_statement(p):
    '''declaration_statement : DCL declaration_list SEMICOL'''
    p[0] = p[2]

def p_declaration_list(p):
    '''declaration_list : declaration 
                        | declaration_list COMMA declaration'''
    if (len(p) == 2):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_declaration(p):
    '''declaration : identifier_list mode 
                   | identifier_list mode initialization'''
    if(len(p) == 2):
        p[0] = Declaration(p[1], p[2])
    else:
        p[0] = Declaration(p[1], p[2], p[3])

def p_initalization(p):
    '''initialization : ASSIGN expression'''
    p[0] = p[1]

def p_identifier_list(p):
    '''identifier_list : identifier 
                       | identifier_list COMMA ID'''
    if(len(p) == 2):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_synonym_statement(p):
    '''synonym_statement : SYN synonym_list SEMICOL'''
    p[0] = p[2]

def p_synonym_list(p):
    '''synonym_list : synonym_definition
                    | synonym_list COMMA synonym_definition'''
    if(len(p) == 2):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

#expression na verdade é constant_expression, entretanto <constant_expression> ::= <expression>
def p_synonym_definition(p):
    '''synonym_definition : identifier_list ASSIGN expression
                          | identifier_list mode ASSIGN expression'''
    if(len(p) == 4):
        p[0] = (p[1],p[3])
    else:
        p[0] = (p[1],p[4],p[2])




def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
