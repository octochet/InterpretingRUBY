from lexer import *
from parser import *
###############################################################################
#                                                                             #
#  INTERPRETER                                                                #
#                                                                             #
###############################################################################

class NodeVisitor(object):
    def visit(self, node):
        method_name = 'visit_' + type(node).__name__
        visitor = getattr(self, method_name, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):
        raise Exception('No visit_{} method'.format(type(node).__name__))

    def visit_Compound(self, node):
        for child in node.children:
            self.visit(child)

    def visit_NoOp(self, node):
        pass


class Interpreter(NodeVisitor):
    GLOBAL_SCOPE = {}
    def __init__(self, parser):
        self.parser = parser
    def visit_String(self, node):
        return node.value
        
    def visit_BinOp(self, node):
        if node.op.type == PLUS:
            return self.visit(node.left) + self.visit(node.right)
        elif node.op.type == MINUS:
            return self.visit(node.left) - self.visit(node.right)
        elif node.op.type == MUL:
            return self.visit(node.left) * self.visit(node.right)
        elif node.op.type == DIV:
            return self.visit(node.left) / self.visit(node.right)
            
    def visit_Boolean_stmt(self, node):
        if node.REL_op.type == EQUALS:
            return (self.visit(node.left) == self.visit(node.right))
        elif node.REL_op.type == LESSTHAN:
            return (self.visit(node.left) < self.visit(node.right))
        elif node.REL_op.type == GREATERTHAN:
            return (self.visit(node.left) > self.visit(node.right))
        elif node.REL_op.type == NOTEQUALS:
            return (self.visit(node.left) != self.visit(node.right))
        elif node.REL_op.type == LESSTHANEQUALS:
            return (self.visit(node.left) <= self.visit(node.right))
        elif node.REL_op.type == GREATERTHANEQUALS:
            return (self.visit(node.left) >= self.visit(node.right))
            
    def visit_If_stmt(self, node):
        if(self.visit(node.condition) == True):
            return self.visit(node.code_block)
        else:
            return self.visit(node.elsecode_block)

    def visit_Unless_stmt(self, node):
        if(self.visit(node.condition) == False):
            return self.visit(node.code_block)

    def visit_While_stmt(self, node):
        if(self.visit(node.condition) == True):
            self.visit(node.code_block)
            return self.visit_While_stmt(node)

    def visit_Until_stmt(self, node):
        if(self.visit(node.condition) == False):
            self.visit(node.code_block)
            return self.visit_Until_stmt(node)
        
            
    
    
    def visit_Num(self, node):
        return node.value
    
    def visit_Assign(self, node):
        var_name = node.left.value
        self.GLOBAL_SCOPE[var_name] = self.visit(node.right)
        
    def visit_Puts(self, node):
        prin = self.visit(node.right)
        print(prin)
        
    def visit_Var(self, node):
        var_name = node.value
        val = self.GLOBAL_SCOPE.get(var_name)
        if val is None:
            raise NameError(repr(var_name))
        else:
            return val

    def interpret(self):
        tree = self.parser.parse()
        return self.visit(tree)


def main():
    while True:
        try:
            try:
                text = input('spi> ')
            except NameError:  # Python3
                text = input('spi> ')
        except EOFError:
            break
        if not text:
            continue

        lexer = Lexer(text)
        parser = Parser(lexer)
        interpreter = Interpreter(parser)
        result = interpreter.interpret()


if __name__ == '__main__':
    main()




