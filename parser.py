from lexer import *
###############################################################################
#                                                                             #
#  PARSER                                                                     #
#                                                                             #
###############################################################################

class AST(object):
    pass

class String(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value
        
class BinOp(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

class If_stmt(AST):
    def __init__(self, condition, code_block , elsecode_block):
        self.condition = condition
        self.code_block = code_block
        self.elsecode_block = elsecode_block

class Unless_stmt(AST):
    def __init__(self, condition, code_block):
        self.condition = condition
        self.code_block = code_block

class While_stmt(AST):
    def __init__(self, condition, code_block):
        self.condition = condition
        self.code_block = code_block

class Until_stmt(AST):
    def __init__(self, condition, code_block):
        self.condition = condition
        self.code_block = code_block
        

class Assign(AST):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right
        
class Boolean_stmt(AST):
    def __init__(self, left, REL_op, right):
        self.left = left
        self.token = self.REL_op = REL_op
        self.right = right
        
class Puts(AST):
    def __init__(self,right):
        self.right = right

class Var(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Num(AST):
    def __init__(self, token):
        self.token = token
        self.value = token.value

class Compound(AST):
    """Represents a List if Statements"""
    def __init__(self):
        self.children = []
class NoOp(AST):
    pass
class Parser(object):
    def __init__(self, lexer):
        self.lexer = lexer
        # set current token to the first token taken from the input
        self.current_token = self.lexer.get_next_token()

    def error(self):
        raise Exception('Invalid syntax')

    def eat(self, token_type):
        # compare the current token type with the passed token
        # type and if they match then "eat" the current token
        # and assign the next token to the self.current_token,
        # otherwise raise an exception.
        if self.current_token.type == token_type:
            self.current_token = self.lexer.get_next_token()
        else:
            self.error()

    def factor(self):
        """factor : INTEGER | LPAREN expr RPAREN | variable|string"""
        token = self.current_token
        if token.type == INTEGER:
            self.eat(INTEGER)
            return Num(token)
        elif token.type == LPAREN:
            self.eat(LPAREN)
            node = self.expr()
            self.eat(RPAREN)
            return node
        elif token.type == STRING:
            node = self.string()
            return node
        else:
            node = self.variable()
            return node

    def term(self):
        """term : factor ((MUL | DIV) factor)*"""
        node = self.factor()

        while self.current_token.type in (MUL, DIV):
            token = self.current_token
            if token.type == MUL:
                self.eat(MUL)
            elif token.type == DIV:
                self.eat(DIV)

            node = BinOp(left=node, op=token, right=self.factor())

        return node

    def expr(self):
        """
        expr   : term ((PLUS | MINUS) term)*
        term   : factor ((MUL | DIV) factor)*

        factor : INTEGER | LPAREN expr RPAREN
        """
        node = self.term()

        while self.current_token.type in (PLUS, MINUS):
            token = self.current_token
            if token.type == PLUS:
                self.eat(PLUS)
            elif token.type == MINUS:
                self.eat(MINUS)

            node = BinOp(left=node, op=token, right=self.term())

        return node
        
    def bol_expr(self):
        """
        boolean_expr : REL_OP expr expr
        """
        
        rel_op = self.current_token
        if(rel_op.type == EQUALS):
            self.eat(EQUALS)
        elif(rel_op.type == LESSTHAN):
            self.eat(LESSTHAN)
        elif(rel_op.type == GREATERTHAN):
            self.eat(GREATERTHAN)
        elif(rel_op.type == LESSTHANEQUALS):
            self.eat(LESSTHANEQUALS)
        elif(rel_op.type == GREATERTHANEQUALS):
            self.eat(GREATERTHANEQUALS)
        elif(rel_op.type == NOTEQUALS):
            self.eat(NOTEQUALS)
            
        left_node = self.expr()
        right_node = self.expr()
        
        node = Boolean_stmt(left = left_node, REL_op = rel_op, right = right_node)
        return node
        
    def program(self):
        """program : compound_statement """
        node = self.compound_statement()
        return node

    
    def compound_statement(self):
        """
        COMPSTMT : STMT {T EXPR} [T]
        """
        nodes = self.statement_list()

        root = Compound()
        for node in nodes:
            root.children.append(node)

        return root


    def statement_list(self):
        """
        statement_list : statement
                    | statement SEMI statement_list
        """
        node = self.statement()

        results = [node]

        while self.current_token.type == SEMI:
            self.eat(SEMI)
            results.append(self.statement())

        if self.current_token.type == ID:
            self.error()

        return results

    def statement(self):
        """
        statement : compound_statement
                | assignment_statement
                | empty
        """

        if self.current_token.type == ID:
            node = self.assignment_statement()
        elif self.current_token.type == 'PUTS':
            node = self.puts_statement()
        elif self.current_token.type == 'IF':
            node = self.if_statement()
        elif self.current_token.type == 'UNLESS':
            node = self.unless_statement()
        elif self.current_token.type == 'WHILE':
            node = self.while_statement()
        elif self.current_token.type == 'UNTIL':
            node = self.until_statement()
        elif self.current_token.type in (EQUALS, LESSTHAN, GREATERTHAN, NOTEQUALS, LESSTHANEQUALS, GREATERTHANEQUALS):
            node = self.bol_expr()
        else:
            node = self.empty()
        return node
    
    def puts_statement(self):
        """puts stat : PUTS expr"""
        self.eat('PUTS')
        if(self.current_token.type in [EQUALS, LESSTHAN, GREATERTHAN, NOTEQUALS, LESSTHANEQUALS, GREATERTHANEQUALS]):
            right = self.bol_expr()
        else:
            right = self.expr()
        node = Puts(right)
        return node


    def if_statement(self):
        """if stat : IF bool_expr THEN comp_stmt {ELSIF bool_expr THEN comp_stmt}ELSE comp_stmt END"""
        self.eat('IF')
        if(self.current_token.type in [EQUALS, LESSTHAN, GREATERTHAN, NOTEQUALS, LESSTHANEQUALS, GREATERTHANEQUALS]):
            condition = self.bol_expr()
            then = self.current_token
            self.eat('THEN')
            compound_stmt = self.compound_statement()
            elsecompound_stmt=None
                
            if(self.current_token.type == "ELSE"):
                self.eat('ELSE')
                elsecompound_stmt = self.compound_statement()
                    
            end = self.current_token
            self.eat('END')
        
        node = If_stmt(condition,compound_stmt,elsecompound_stmt)
      
  
        return node


    def unless_statement(self):
        """unless stat : UNLESS bool_expr THEN comp_stmt END"""
        self.eat('UNLESS')
        if(self.current_token.type in [EQUALS, LESSTHAN, GREATERTHAN, NOTEQUALS, LESSTHANEQUALS, GREATERTHANEQUALS]):
            condition = self.bol_expr()
            then = self.current_token
            self.eat('THEN')
            compound_stmt = self.compound_statement()
            end = self.current_token
            self.eat('END')
        
        node = Unless_stmt(condition,compound_stmt)
      
  
        return node

    def while_statement(self):
        """while stat : WHILE bool_expr DO comp_stmt END"""
        self.eat('WHILE')
        if(self.current_token.type in [EQUALS, LESSTHAN, GREATERTHAN, NOTEQUALS, LESSTHANEQUALS, GREATERTHANEQUALS]):
            condition = self.bol_expr()
            does = self.current_token
            self.eat('DO')
            compound_stmt = self.compound_statement()
            end = self.current_token
            self.eat('END')
        
        node = While_stmt(condition,compound_stmt)
      
  
        return node

    def until_statement(self):
        """until stat : UNTIL bool_expr DO comp_stmt END"""
        self.eat('UNTIL')
        if(self.current_token.type in [EQUALS, LESSTHAN, GREATERTHAN, NOTEQUALS, LESSTHANEQUALS, GREATERTHANEQUALS]):
            condition = self.bol_expr()
            does = self.current_token
            self.eat('DO')
            compound_stmt = self.compound_statement()
            end = self.current_token
            self.eat('END')
        
        node = Until_stmt(condition,compound_stmt)
      
  
        return node

        
    def assignment_statement(self):
        """
        assignment_statement : variable ASSIGN_OP expr
        """
        left = self.variable()
        token = self.current_token
        self.eat(ASSIGN_OP)
        right = self.expr()
        node = Assign(left, token, right)
        return node

    def empty(self):
        """An empty production"""
        return NoOp()

    def variable(self):
        """
        variable : ID
        """
        node = Var(self.current_token)
        self.eat(ID)
        return node
        
    def string(self):
        """ stirng """
        node = String(self.current_token)
        self.eat(STRING)
        return node
        
    def parse(self):
        node = self.program()
        if self.current_token.type != EOF:
            self.error()

        return node



