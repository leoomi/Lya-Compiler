# ------------------------------------------------------------
# lyalex.py
# ------------------------------------------------------------
import ply.lex as lex
import sys

# List of token names.   This is always required
tokens = [
        'ASSIGN',
        'AND',
        'OR',
        'EQUALS',
        'DIFF',
        'GT',
        'GE',
        'LS',
        'LE',
        'CONCAT',
        'ICONST',
        'SCONST',
        'CCONST',
        'PLUS',
        'MINUS',
        'NOT',
        'TIMES',
        'DIVIDE',
        'LPAREN',
        'RPAREN',
        'COMMA',
        'COMMENT',
        'MOD',
        'SEMICOL',
        'RBRACKET',
        'LBRACKET',
        'COLON',
        'PLUSEQ',
        'MINUSEQ',
        'TIMESEQ',
        'DIVIDEEQ',
        'CONCATEQ', 
        'ID'
]

reserved = {
        'array': 'ARRAY',
        'by': 'BY',
        'chars': 'CHARS', 
        'dcl': 'DCL', 
        'do': 'DO', 
        'down': 'DOWN',
        'else': 'ELSE',
        'elsif': 'ELSIF',
        'end': 'END',
        'exit': 'EXIT',
        'fi': 'FI',
        'for': 'FOR',
        'if': 'IF', 
        'in': 'IN', 
        'loc': 'LOC',
        'type': 'TYPE',
        'od': 'OD',
        'proc': 'PROC',
        'ref': 'REF', 
        'result': 'RESULT',
        'return': 'RETURN',
        'returns': 'RETURNS',
        'syn': 'SYN',
        'then': 'THEN',
        'to': 'TO',
        'while': 'WHILE',
        'abs': 'ABS', 
        'asc': 'ASC',
        'bool': 'BOOL',
        'char': 'CHAR',
        'false': 'FALSE',
        'int': 'INT',
        'length': 'LENGTH',
        'lower': 'LOWER',
        'null': 'NULL',
        'num': 'NUM',
        'print': 'PRINT',
        'read': 'READ',
        'true': 'TRUE',
        'upper': 'UPPER'
}

tokens += list(reserved.values())

# Regular expression rules for simple tokens
t_PLUS    = r'\+'
t_MINUS   = r'-'
t_TIMES   = r'\*'
t_DIVIDE  = r'/'
t_LPAREN  = r'\('
t_RPAREN  = r'\)'
t_COMMA = r','
t_SEMICOL = r';'
t_ASSIGN = r'='
t_NOT = r'\!'
t_MOD = r'\%'
t_CONCAT = r'&'
t_AND = r'&&'
t_OR = r'\|\|'
t_EQUALS = r'=='
t_DIFF = r'\!='
t_GT = r'>'
t_GE = r'>='
t_LS = r'<'
t_LE = r'<='
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_COLON = r':'
t_PLUSEQ = r'\+='
t_MINUSEQ = r'\-='
t_TIMESEQ = r'\*='
t_DIVIDEEQ = r'/='
t_CONCATEQ = r'&='

def t_COMMENT(t):
    r'(/\*[\s\S]*\*/)|(//.*)'
    pass

def t_ICONST(t):
    r'\d+'
    t.value = int(t.value)                    
    return t

def t_SCONST(t):
    r'\"([^"\\\n]|\\.)*\"'
    return t

def t_CCONST(t):
    r"\'([^']|\\.)\'"
    return t

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Rule for handling identifiers (and possibly reserved words) 
def t_ID(t):
    r'[a-zA-Z_][a-zA-Z_0-9]*'
    t.type = reserved.get(t.value,'ID')    # Check for reserved words
    return t

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

def t_unterminatedString(t):
    r'\".*'
    print("%d: Unterminated string" % t.lineno);
    pass

def t_unterminatedComment(t):
    r'/\*[\s\S]*$'
    print("%d: Unterminated comment" % t.lineno);
    pass

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

"""
# Test it out
data = '''
/* Compute the fatorial of an integer */

fat: proc (n int) returns (int);
  if n==0 then
    return 1;
  else
    return n * fat (n-1);
  fi;
end;/*
dcl x int;
print("give-me a positive integer:);
read(x);
print("fatorial of" , x, " = ", fat(x));
'''
"""
def main():
    # Open file
    file = sys.argv[1]
    data = open(file)

    # Build the lexer
    lexer = lex.lex()

    # Give the lexer some input
    lexer.input(data.read())

    # Tokenize
    while True:
        tok = lexer.token()
        if not tok: 
            break      # No more input
        print(tok)
        
if __name__ == "__main__":
    # execute only if run as a script
    main()
