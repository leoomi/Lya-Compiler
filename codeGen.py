class CodeGen(object):
    def generate(self, program):
        self.varsRefs = {}
        for field in getattr(program, "_fields"):
            print(field)
