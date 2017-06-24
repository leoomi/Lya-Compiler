from lyaparser import *

while True:
      try:
          s = input('calc > ')
      except EOFError:
          break
      if not s: continue
      result = parser.parse(s)
      visit = visitor.visit(result)
