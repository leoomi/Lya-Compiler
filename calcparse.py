# Yacc example

import ply.yacc as yacc
import ply.lex as lex

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

class Value_array_element:
    def __init__(self, array_primitive_value, expression_list):
        self.array_primitive_value = array_primitive_value
        self.expression_list = expression_list

class Value_array_slice:
    def __init__(self, array_primitive_value, lower_element, upper_element):
        self.array_primitive_value = array_primitive_value  
        self.lower_element = lower_element
        self.upper_element = upper_element 

class Conditional_expression:
    def __init__(self, boolean_expression, then_expression, else_expression, elsif_expression=None):
        self.boolean_expression = boolean_expression
        self.then_expression = then_expression
        self.else_expression = else_expression
        self.elsif_expression = elsif_expression

class Procedure_definition:
    def __init__(self, formal_parameter_list=None, result_spec=None, statement_list=None):
        self.formal_paremeter = formal_parameter_list
        self.result_spec = result_spec
        self.statement_list = statement_list

class Builtin_call:
    def __init__(self, builtin_name, parameter_list=None):
        self.builtin_name = builtin_name
        self.parameter_list = parameter_list

class Procedure_call:
    def __init__(self, ID, parameter_list=None):
        self.ID = ID
        self.parameter_list = parameter_list

class Step_enumeration:
    def __init__(self, loop_counter, assignment_symbol, start_value, end_value, step_value=None, down=None):
        self.loop_counter = loop_counter
        self.assignment_symbol = assignment_symbol
        self.start_value = start_value
        self.end_value = end_value
        self.step_value = step_value
        self.down = down

class Control_part:
    def __init__(self, for_control=None, while_control=None):
        self.for_control = for_control
        self.for_control = while_control
        
class Elsif_expression:
    def __init__(self, boolean_expression, then_expression, elsif_expression=None):
        self.boolean_expression = boolean_expression
        self.then_expression = then_expression
        self.elsif_expression = elsif_expression

class Operand0:
    def __init__(self, operand1, operand0=None, operator1=None):
        self.operand1 = operand1     
        self.operand0 = operand0
        self.operator1 = operator1

class Operand1:
    def __init__(self, operand2, operand1=None, operator2=None):
        self.operand2 = operand2
        self.operand1 = operand1
        self.operator2 = operator2

class Operand2:
    def __init__(self, operand3, operand2=None, arithmetic_multiplicative_operator=None):
        self.operand3 = operand3
        self.operand2 = operand2
        self.arithmetic_multiplicative_operator = arithmetic_multiplicative_operator

class Operand3:
    def __init__(self, operandOrLiteral, monadic_operator=None):
        self.operandOrLiteral = operandOrLiteral
        self.monadic_operator = monadic_operator

class Action_statement:
    def __init__(self, action, label_id=None):
        self.action = action
        self.label_id = label_id

class Assigning_operator:
    def __init__(self, assignment_symbol, closed_dyadic_operator=None):
        self.closed_dyadic_operator = closed_dyadic_operator
        self.assignment_symbol = assignment_symbol

class If_action:
    def __init__(self, boolean_expression, then_clause, else_clause=None):
        self.boolean_expression = boolean_expression
        self.closed_dyadic_operator = closed_dyadic_operator

class Else_clause:
    def __init__(self, boolean_expression=None, then_clause=None, else_clause=None, many_action_statement=None):
        self.boolean_expression = boolean_expression
        self.then_clause = then_clause
        self.else_clause = else_clause
        self.many_action_statement = many_action_statement

def p_program(p):
    'program : statement_list'
    p[0] = ("program",p[1])

def p_statement_list(p):
    '''statement_list : statement 
                      | statement_list statement'''
    if (len(p) == 2):
        p[0] = ("list-statement",[p[1]])
    else:
        p[0] = ("list-statement",p[1] + [p[2]])

def p_statement(p):
    '''statement : declaration_statement
                 | synonym_statement
                 | newmode_statement
                 | procedure_statement
                 | action_statement'''
    p[0] = ("statement",p[1])

def p_declaration_statement(p):
    '''declaration_statement : DCL declaration_list SEMICOL'''
    p[0] = ("statement_declaration",p[2])

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
    if(len(p) == 3):
        p[0] = Declaration(p[1], p[2])
    else:
        p[0] = Declaration(p[1], p[2], p[3])

def p_initalization(p):
    '''initialization : ASSIGN expression'''
    p[0] = p[1]

def p_identifier_list(p):
    '''identifier_list : ID 
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
    else:
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
    '''mode_name : ID'''
    p[0] = p[1]

def p_discrete_mode_name(p):
    '''discrete_mode_name : ID'''
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
    else:
        p[0] = p[1] + [p[3]]

def p_index_mode(p):
    '''index_mode : discrete_mode 
                  | literal_range'''
    p[0] = p[1]

def p_element_mode(p):
    '''element_mode : mode'''
    p[0] = p[1]

def p_location(p):
    '''location : string_location 
                | dereferenced_reference
                | string_element
                | string_slice
                | array_element
                | array_slice
                | call_action'''
    p[0] = p[1]

def p_dereferenced_reference(p):
    '''dereferenced_reference : location ARROW'''
    p[0] = p[1]

def p_string_element(p):
    '''string_element : string_location LBRACKET start_element RBRACKET'''
    p[0] = (p[1],p[3])

def p_start_element(p):
    '''start_element : integer_expression'''
    p[0] = p[1]

def p_string_slice(p):
    '''string_slice : string_location LBRACKET left_element COLON right_element RBRACKET'''
    p[0] = (p[1], p[3], p[5])

def p_string_location(p):
    '''string_location : ID'''
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

def p_empty_literal(p):
    '''empty_literal : NULL'''
    p[0] = p[1]

def p_character_string_literal(p):
    '''character_string_literal : SCONST'''
    p[0] = p[1]


def p_value_array_element(p):
    '''value_array_element : array_primitive_value LBRACKET expression_list RBRACKET'''
    p[0] = Value_array_element(p[1],p[3])

def p_value_array_slice(p):
    '''value_array_slice : array_primitive_value LBRACKET ICONST COLON ICONST RBRACKET'''
    p[0] = Value_array_slice(p[1],p[3],p[5])

def p_array_primitive_value(p):
    '''array_primitive_value : primitive_value'''
    p[0] = p[1]

def p_parenthesized_expression(p):
    '''parenthesized_expression : LPAREN expression RPAREN'''
    p[0] = p[2]

def p_expression(p):
    '''expression : operand0 
                  | conditional_expression'''
    p[0] = p[1]

def p_integer_expression(p):
    '''integer_expression : expression'''
    p[0] = p[1]

def p_conditional_expression(p):
    '''conditional_expression : IF boolean_expression then_expression else_expression FI
                              | IF boolean_expression then_expression elsif_expression else_expression FI'''
    if(len(p) == 6):
        p[0] = Conditional_expression(p[2],p[3],p[4])
    else:
        p[0] = Conditional_expression(p[2],p[3],p[5],p[4])


def p_boolean_expression(p):
    '''boolean_expression : expression'''
    p[0] = p[1]

def p_then_expression(p):
    '''then_expression : THEN expression'''
    p[0] = p[2]

def p_else_expression(p):
    '''else_expression : ELSE expression'''
    p[0] = p[2]

def p_elsif_expression(p):
    '''elsif_expression : ELSIF boolean_expression then_expression
                        | elsif_expression ELSIF boolean_expression then_expression'''
    if (len(p) == 4): 
        p[0] = Elsif_expression(p[2],p[3])
    else:
        p[0] = Elsif_expression(p[3],p[4],p[1])

def p_operand0(p):
    '''operand0 : operand1
                | operand0 operator1 operand1'''
    if(len(p) == 2):
        p[0] = Operand0(p[1])
    else:
        p[0] = Operand0(p[3],p[1],p[2])

def p_operator1(p):
    '''operator1 : relational_operator
                 | membership_operator'''
    p[0] = p[1]

def p_relational_operator(p):
    '''relational_operator : AND 
                           | OR 
                           | EQUALS
                           | DIFF 
                           | GT 
                           | GE 
                           | LS 
                           | LE'''
    p[0] = p[1]
    
def p_membership_operator(p):
    '''membership_operator : IN'''
    p[0] = p[1]

def p_operand1(p):
    '''operand1 : operand2
                | operand1 operator2 operand2'''
    if (len(p) == 2):
        p[0] = Operand1(p[1])
    else:
        p[0] = Operand1(p[3],p[1],p[2])

def p_operator2(p):
    '''operator2 : arithmetic_additive_operator
                 | string_concatenation_operator'''
    p[0] = p[1]

def p_arithmetic_additive_operator(p):
    '''arithmetic_additive_operator : PLUS
                                    | MINUS'''
    p[0] = p[1]

def p_string_concatenation_operator(p):
    '''string_concatenation_operator : CONCAT'''
    p[0] = p[1]

def p_operand2(p):
    '''operand2 : operand3
                | operand2 arithmetic_multiplicative_operator operand3'''
    if (len(p) == 2):
        p[0] = Operand2(p[1])
    else:
        p[0] = Operand2(p[3],p[1],p[2])

def p_arithmetic_multiplicative_operator(p):
    '''arithmetic_multiplicative_operator : TIMES 
                                          | DIVIDE
                                          | MOD'''
    p[0] = p[1]

def p_operand3(p):
    '''operand3 : monadic_operator operand4
                | operand4'''
    if (len(p) == 3):
        p[0] = Operand3(p[2], p[1])
    else:
        p[0] = Operand3(p[1])

def p_monadic_operator(p):
    '''monadic_operator : MINUS
                        | NOT'''
    p[0] = p[1]

def p_operand4(p):
    '''operand4 : location
                | referenced_location
                | primitive_value'''
    p[0] = p[1]

def p_referenced_location(p):
    '''referenced_location : ARROW location'''
    p[0] = p[2]

def p_action_statement(p):
    '''action_statement : label_id COLON action SEMICOL
                        | action SEMICOL'''
    if (len(p) == 5):
        p[0] = Action_statement(p[3],p[1])
    else:
        p[0] = Action_statement(p[1])

def p_do_action(p):
    '''do_action : DO control_part SEMICOL OD
                 | DO control_part SEMICOL many_action_statement OD
                 | DO many_action_statement OD
                 | DO OD
                 '''

def p_control_part(p):
    '''control_part : for_control while_control
                    | for_control
                    | while_control'''
    if(len(p) == 3):
        p[0] = Control_part(p[1], p[2])
    elif(len(p) == 2):
        if(p[1][0] == 'while_control'):
            p[0] = Control_part(while_control = p[1])
        else:
            p[0] = Control_part(for_control = p[1])

def p_for_control(p):
    '''for_control : FOR iteration'''
    p[0] = ('for_control', p[2])

def p_interation(p):
    '''iteration : step_enumeration
                 | range_enumeration'''
    p[0] = p[1]

def p_step_enumeration(p):
    '''step_enumeration : loop_counter assignment_symbol start_value step_value DOWN end_value
                        | loop_counter assignment_symbol start_value DOWN end_value
                        | loop_counter assignment_symbol start_value step_value end_value
                        | loop_counter assignment_symbol start_value end_value'''
    if(len(p) == 7):
        p[0] = Step_enumeration(p[1], p[2], p[3], p[6], p[4], p[5])
    elif(len(p) == 6):
        if(p[4] == 'DOWN'):
            p[0] = Step_enumeration(p[1], p[2], p[3], p[6], )
        else:
            p[0] = Step_enumeration(p[1], p[2], p[3], p[6], )
    elif(len(p) == 5):
        p[0] = Step_enumeration(p[1], p[2], p[3], p[6])
    

def p_loop_counter(p):
    '''loop_counter : ID'''
    p[0] = p[1]

def p_start_value(p):
    '''start_value : discrete_expression'''
    p[0] = p[1]

def p_step_value(p):
    '''step_value : BY integer_expression'''
    p[0] = p[2]

def p_end_value(p):
    '''end_value : TO discrete_expression'''
    p[0] = p[2]

def p_discrete_expression(p):
    '''discrete_expression :  expression'''
    p[0] = p[1]

def p_label_id(p):
    '''label_id : ID'''
    p[0] = p[1]

def p_action(p):
    '''action : bracketed_action
              | assignment_action
              | call_action
              | exit_action
              | return_action
              | result_action'''
    p[0] = p[1]

def p_bracketed_action(p):
    '''bracketed_action : if_action 
                        | do_action'''
    p[0] = p[1]

def p_assignment_action(p):
    '''assignment_action : location assigning_operator expression'''
    p[0] = (p[1], p[2], p[3])

def p_assigning_operator(p):
    '''assigning_operator : closed_dyadic_operator assignment_symbol
                          | assignment_symbol'''
    if (len(p) == 3):
        p[0] = Assigning_operator(p[2],p[1])
    else:
        p[0] = Assigning_operator(p[1])

def p_closed_dyadic_operator(p):
    '''closed_dyadic_operator : arithmetic_additive_operator
                              | arithmetic_multiplicative_operator
                              | string_concatenation_operator'''
    p[0] = p[1]

def p_assignment_symbol(p):
    '''assignment_symbol : ASSIGN'''
    p[0] = p[1]

def p_if_action(p):
    '''if_action : IF boolean_expression then_clause else_clause FI
                 | IF boolean_expression then_clause FI'''
    if (len(p) == 6):
        p[0] = If_action(p[2],p[3],p[4])
    else:
        p[0] = If_action(p[2],p[3])

def p_then_clause(p):
    '''then_clause : THEN many_action_statement
                   | THEN'''
    if (len(p) == 3):
        p[0] = (p[1],p[2])
    else:
        p[0] = (p[1],None)

def p_many_action_statement(p):
    '''many_action_statement : action_statement
                             | many_action_statement action_statement'''
    if (len(p) == 2):
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_else_clause(p):
    '''else_clause : ELSE many_action_statement
                   | ELSE
                   | ELSIF boolean_expression then_clause else_clause
                   | ELSIF boolean_expression then_clause'''
    if (len(p) == 2):
        p[0] = Else_clause()
    elif (len(p) == 3):
        p[0] = Else_clause(many_action_statement = p[2])
    elif (len(p) == 4):
        p[0] = Else_clause(p[2],p[3])
    else:
        p[0] = Else_clause(p[2],p[3],p[4])

def p_range_enumeration(p):
    '''range_enumeration : loop_counter IN discrete_mode
                         | loop_counter DOWN IN discrete_mode'''
    if(len(p) == 4):
        p[0] = (p[1], None, discrete_mode)
    else:
        p[0] = (p[1], 'DOWN', discrete_mode)

def p_while_control(p):
    '''while_control : WHILE boolean_expression'''
    p[0] = ('while_control', p[2])

def p_call_action(p):
    '''call_action : procedure_call
                   | builtin_call'''
    p[0] = p[1]

def p_procedure_call(p):
    '''procedure_call : ID LPAREN RPAREN
                      | ID LPAREN parameter_list RPAREN'''
    if(len(p) == 4):
        p[0] = Procedure_call(p[1])
    else:
        p[0] = Procedure_call(p[1], p[3])

def p_parameter_list(p):
    '''parameter_list : parameter
                      | parameter COMMA parameter_list'''
    if (len(p) == 2):
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[3]

def p_parameter(p):
    '''parameter : expression'''
    p[0] = p[1]

def p_exit_action(p):
    '''exit_action : EXIT label_id'''
    p[0] = p[2]
    
def p_return_action(p):
    '''return_action : RETURN
                     | RETURN result'''
    if(len(p) == 2):
        p[0] = (p[1], None)
    else:
        p[0] = (p[1], p[2])
    
def p_result_action(p):
    '''result_action : RESULT result'''
    p[0] = p[2]
    
def p_result(p):
    '''result : expression'''
    p[0] = p[1]
    
def p_builtin_call(p):
    '''builtin_call : builtin_name LPAREN RPAREN
                    | builtin_name LPAREN parameter_list RPAREN'''
    if(len(p) == 3):
        p[0] = Builtin_call(p[1])
    else:
        p[0] = Builtin_call(p[1], p[3])
    
def p_builtin_name(p):
    '''builtin_name : ABS
                    | ASC
                    | NUM
                    | UPPER
                    | LOWER
                    | LENGTH
                    | READ
                    | PRINT'''

    p[0] = p[1]
    
def p_procedure_statement(p):
    '''procedure_statement : label_id COLON procedure_definition SEMICOL'''
    p[0] = (p[1], p[3])
    
def p_procedure_definition(p):
    '''procedure_definition : PROC LPAREN RPAREN SEMICOL END
                            | PROC LPAREN RPAREN SEMICOL statement_list END
                            | PROC LPAREN formal_parameter_list RPAREN SEMICOL END
                            | PROC LPAREN RPAREN result_spec SEMICOL END
                            | PROC LPAREN RPAREN result_spec SEMICOL statement_list END
                            | PROC LPAREN formal_parameter_list RPAREN SEMICOL statement_list END
                            | PROC LPAREN formal_parameter_list RPAREN result_spec SEMICOL END
                            | PROC LPAREN formal_parameter_list RPAREN result_spec SEMICOL statement_list END'''
    if(len(p) == 8):
        p[0] = Procedure_definition(p[3], p[5], p[7])
    elif(len(p) == 7):
        if(p[3] == 'RPAREN'):
            p[0] = Procedure_definition(result_spec = p[4], statement_list = p[6])
        elif(p[5] == 'SEMICOL'):
            p[0] = Procedure_definition(formal_parameter_list = p[3], statement_list = p[6])
        else:
            p[0] = Procedure_definition(formal_parameter_list = p[3], result_spec = p[5])
    elif(len(p) == 6):
        if(p[3] == 'RPAREN' and p[5] == 'SEMICOL'):
            p[0] = Procedure_definition(result_spec = p[4])
        elif(p[3] == 'RPAREN'):
            p[0] = Procedure_definition(formal_paramenter_list = p[3])
        else:
            p[0] = Procedure_definition(statement_list = p[5])
    elif(len(p) == 5):
        p[0] = Procedure_definition()
        
        
        
def p_formal_parameter_list(p):
    '''formal_parameter_list : formal_parameter
                             | formal_parameter_list COMMA formal_parameter'''
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

def p_result_spec(p):
    '''result_spec : RETURNS LPAREN mode RPAREN
                          | RETURNS LPAREN mode result_attribute RPAREN'''
    if(len(p) == 5):
        p[0] = Result_spec(p[3])
    else:
        p[0] = Result_spec(p[3], p[4])

def p_result_attribute(p):
    '''result_attribute : LOC'''
    p[0] = p[1]
    
def p_error(p):
    print("Syntax error in input!")

# Build the parser
parser = yacc.yacc()
parser.lexer = lex.lex(object=Lyalex())

while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)
