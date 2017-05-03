import os
import sys
from lyaparser import *

fpath = sys.argv[-1]

with open (fpath, "r") as myfile:
    data=myfile.read().replace('\n', '')

result = parser.parse(data)
visit = visitor.visit(result)
