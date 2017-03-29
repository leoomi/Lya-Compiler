# Yacc example

import ply.yacc as yacc

# Get the token map from the lexer.  This is required.
from lyalex import Lyalex

tokens = Lyalex().tokens

class Declaration:
    def __init__(self, identifier_list, mode, value=None):
        self.identifier_list = identifier_list
        self.mode = mode
        self.value = value

class Synonym_definition:
    def __init__(self, identifier_list, constant_expression, mode=None):
        self.identifier_list = identifier_list
        self.mode = mode
        self.constant_expression = constant_expression

class Mode_definition:
    def __init__(self, identifier_list, mode):
        self.identifier_list = identifier_list
        self.mode = mode

class Returns_definition:
    def __init__(self, mode, result_attribute=None):
        self.mode = mode;
        self.result_attribute = result_attribute

class Parameter_spec:
    def __init__(self, mode, parameter_attribute=None):
        self.mode = mode
        self.parameter_attribute = parameter_attribute

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

def p_synonym_definition(p):
    '''synonym_definition : identifier_list ASSIGN constant_expression
                          | identifier_list mode ASSIGN constant_expression'''
    if(len(p) == 4):
        p[0] = Synonym_definition(p[1],p[3])
    else:
        p[0] = Synonym_definition(p[1],p[4],p[2])

def p_constant_expression(p):
    '''constant_expression : expression'''
    p[0] = p[1]

def p_newmode_statement(p): 
    '''newmode_statement : TYPE newmode_list SEMICOL'''
    p[0] = p[2]

def p_newmode_list(p):
    '''newmode_list : mode_definition
                    | newmode_list COMMA mode_definition'''
    if(len(p) == 2):
        p[0] = [p[1]]
    else
        p[0] = p[1] + [p[3]]

def p_mode_definition(p): 
    '''mode_definition : identifier_list ASSIGN mode'''
    p[0] = Mode_definition(p[1],p[3])

def p_mode(p):
    '''mode : mode_name
            | discrete_mode
            | reference_mode
            | composite_mode'''
    p[0] = p[1]

def p_discrete_mode(p):
    '''discrete_mode : integer_mode
                     | boolean_mode
                     | character_mode
                     | discrete_range_mode'''
    p[0] = p[1]

def p_integer_mode(p):
    '''integer_mode : INT'''
    p[0] = p[1]

def p_boolean_mode(p):
    '''boolean_mode : BOOL'''
    p[0] = p[1]

def p_character_mode(p):
    '''character_mode : CHAR'''
    p[0] = p[1]

def p_discrete_range_mode(p):
    '''discrete_range_mode : discrete_mode_name LPAREN literal_range RPAREN
                           | discrete_mode LPAREN literal_range RPAREN'''
    p[0] = (p[1], p[3])

def p_mode_name(p):
    '''mode_name : identifier'''
    p[0] = p[1]

def p_discrete_mode_name(p):
    '''discrete_mode_name : identifier'''
    p[0] = p[1]

def p_literal_range(p):
    '''literal_range : lower_bound COLON upper_bound'''
    p[0] = (p[1],p[3])

def p_lower_bound(p):
    '''lower_bound : expression'''
    p[0] = p[1]

def p_upper_bound(p):
    '''upper_bound : expression'''
    p[0] = p[1]

def p_reference_mode(p):
    '''reference_mode : REF mode'''
    p[0] = p[2]

def p_composite_mode(p):
    '''composite_mode : string_mode 
                      | array_mode'''
    p[0] = p[1]

def p_string_mode(p):
    '''string_mode : CHARS LBRACKET string_length RBRACKET'''
    p[0] = p[3]

def p_string_length(p):
    '''string_length : integer_literal'''
    p[0] = p[1]

def p_array_mode(p):
    '''array_mode : ARRAY LBRACKET index_mode_list RBRACKET element_mode'''
    p[0] = (p[3],p[5])

def p_index_mode_list(p):
    '''index_mode_list : index_mode
                       | index_mode_list COMMA index_mode'''
    if(len(p) == 2):
        p[0] = [p[1]]
    else
        p[0] = p[1] + [p[3]]

def p_index_mode(p):
    '''index_mode : discrete_mode 
                  | literal_range'''
    p[0] = p[1]

def p_element_mode(p):
    '''element_mode : mode'''
    p[0] = p[1]

def p_location(p):
    '''location : location_name
                | dereferenced_reference
                | string_element
                | string_slice
                | array_element
                | array_slice
                | call_action'''
    p[0] = p[1]

def dereferenced_reference(p):
    '''dereferenced_reference : location ARROW'''
    p[0] = p[1]

def string_element(p):
    '''string_element : string_location LBRACKET start_element RBRACKET'''
    p[0] = (p[1],p[3])

def p_start_element(p):
    '''start_element : integer_expression'''
    p[0] = p[1]

def p_string_slice(p):
    '''string_slice : string_location LBRACKET left_element COLON right_element RBRACKET'''
    p[0] = (p[1], p[3], p[5])

def p_string_location(p):
    '''string_location : identifier'''
    p[0] = p[1]

def p_left_element(p):
    '''left_element : integer_expression'''
    p[0] = p[1]

def p_right_element(p):
    '''right_element : integer_expression'''
    p[0] = p[1]

def p_array_element(p):
    '''array_element : array_location LBRACKET expression_list RBRACKET'''
    p[0] = (p[1], p[3])

def p_expression_list(p):
    '''expression_list : expression
                       | expression_list COMMA expression'''
    if(len(p) == 2):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_array_slice(p):
    '''array_slice : array_location LBRACKET lower_bound COLON upper_bound RBRACKET'''
    p[0] = (p[1], p[3], p[5])

def p_array_location(p):
    '''array_location : location'''
    p[0] = p[1]

def p_primitive_value(p):
    '''primitive_value : literal
                       | value_array_element
                       | value_array_slice
                       | parenthesized_expression'''
    p[0] = p[1]

def p_literal(p):
    '''literal : integer_literal
               | boolean_literal
               | character_literal
               | empty_literal
               | character_string_literal'''
    p[0] = p[1]

def p_integer_literal(p):
    '''integer_literal :  ICONST'''
    p[0] = p[1]

def p_boolean_literal(p):
    '''boolean_literal : FALSE 
                       | TRUE'''
    p[0] = p[1]

def p_character_literal(p):
    '''character_literal : CCONST
                         | APOSTH CARET LPAREN ICONST RPAREN APOSTH'''
    if(len(p) == 2):
        p[0] = p[1]
    else:
        p[0] = p[4]

def empty_literal(p):
    '''empty_literal : NULL'''
    p[0] = p[1]

def character_string_literal(p):
    '''character_string_literal : SCONST'''
    p[0] = p[1]


#CONTINUE FROM HERE ROGER!


def p_procedure_definition(p):
    '''procedure_definition : PROC RPAREN LPAREN SEMICOL END
                            | PROC RPAREN formal_parameter_list '''
        
def p_formal_parameter_list(p):
    '''formal_parameter_list : formal_parameter
                             | formal_paramenter_list COMMA formal_parameter'''
    if(len(p) == 2):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]
        
def p_formal_parameter(p):
    '''formal_parameter : identifier_list parameter_spec'''
    p[0] = (p[1], p[2])
        
def p_paremeter_spec(p):
    '''parameter_spec : mode
                      | mode parameter_attribute'''
    if(len(p) == 2):
        p[0] = Parameter_spec(p[1])
    else:
        p[0] = Parameter_spec(p[1], p[2])
        
def p_paremeter_attribute(p):
    '''parameter_attribute : LOC'''
    p[0] = p[1]

def p_returns_definition(p):
    '''returns_definition : RETURNS LPAREN mode RPAREN
                          | RETURNS LPAREN mode result_attribute RPAREN'''
    if(len(p) == 5):
        p[0] = Returns_definition(p[3])
    else:
        p[0] = Returns_definition(p[3], p[4])

def p_result_attribute(p):
    '''result_attribute : LOC'''
    p[0] = p[1]
    
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
