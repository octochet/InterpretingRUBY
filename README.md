# Ruby-Interpreter
Designing a basic interpreter for RUBY in PYTHON

## Brief Description
This Ruby interpreter takes one line at a time as input from the user, interprets it and produces the output. And then waits for next line of input to be entered. Next line is the continuation of the first line and so on.
It has three main files Lexer, Parser, Interpreter.

[*Lexer*](#lexer) - It takes the given Line as String and returns the tokens present in it. It has predefined Token types, Reserved keywords. It has two classes 'Token' and 'Lexer'.

[*Parser*](#parser) - It gets the tokens of the given line from [Lexer](#lexer) and makes an Abstract syntax tree based on it.

[*Interpreter*](#interpreter) - It gets the abstract syntax tree from [Parser](#parser) and interprets the tree based on the semantics of the Ruby.

### Subset of the BNF used:

PROGRAM : COMPSTMT

T : ";" | "\n"

COMPSTMT : STMT {T EXPR} \[T]
 
statement_list : statement| statement SEMI statement_list

statement : compound_statement
                | assignment_statement
                | empty

factor : INTEGER | LPAREN expr RPAREN | variable|string

term : factor ((MUL | DIV) factor)*

expr   : term ((PLUS | MINUS) term)*
 
boolean_expr : REL_OP expr expr

if stat : IF bool_expr THEN comp_stmt {ELSIF bool_expr THEN comp_stmt}ELSE comp_stmt END  

puts stat : PUTS expr

unless stat : UNLESS bool_expr THEN comp_stmt END

while stat : WHILE bool_expr DO comp_stmt END

until stat : UNTIL bool_expr DO comp_stmt END

assignment_statement : variable ASSIGN_OP expr

# Lexer
The predefined token types present in Lexer file are INTEGER, PLUS, MINUS, MUL, DIV, LPAREN, RPAREN, EOF,ID, ASSIGN_OP, SEMI,STRING, EQUALS, LESSTHAN, GREATERTHAN, NOTEQUALS, LESSTHANEQUALS, GREATERTHANEQUALS. The Reseved Keywords present are  'end', 'if', 'else', 'elsif', 'then', 'while', 'unless', 'do', 'puts', 'until'.

It has a 'Token' class to define the tokens used. And a 'Lexer' class to check and return the token types present in the given string. It has the following functions defined in it.

### *error*  
It raises an exception called "Invalid Character" whenever the function is called.

### *peek*  
It returns what character is present next to the pointer but doesn't change the pointers location.

### *_id*  
It checks if the word given is in Reserved keywords and returns it. If it is not present then it is returned as 'ID' Token. 

### *advance* 
It forwards the pointer. If it reaches the end of the input then current character is 'None', else it is the character at the pointer.

### *skip_whitespace*  
It skips the whitespace character if the pointer points at whitespaces.

### *integer* 
It returns the integer value if the pointer points at any multidigit integer.

### *string*  
It returns all the characters until ' " ' is encountered and skips the character ' " '.

### *get_next_token*  
It is Lexical analyser. If the pointer is at whitespace, it skips that character by calling [*skip_whitespace*](#skip_whitespace) and continues to run rest of the code. If the pointer is at alphabet, it calls [*_id*](#_id) functions and returns the corresponding token. If the pointer is at interger, it calls [*integer*](#integer) and returns corresponding integer. If the pointer is at one of the predefined tokentypes then it returns those corresponding token objects. If the pointer is not present in any one of the above then it calls [*error*](#error) and the program stops. When end of the input, that is, 'None' is encountered then it returns 'EOF' Token.

# Parser
It has different classes to define an abstract syntax tree and a class *Parser* that parses the given string. It imports all the classes and methods of [*Lexer*](#lexer).

Different classes to create Abstract Syntax Tree:

A empty class **AST** that is an abstraction of all its derived classes. And its derived classes are: 
1. class *String* - stores token type of String.
2. class *BinOp* - stores left value to an operator 'op' and also the operator and its right value.
3. class *If_stmt* - stores a condition, code_block and elsecode_block of an If statement.
4. class *Unless_stmt* - stores a condition and a code_block of an UNLESS statement.
5. class *While_stmt* - stores a conditon and a code_block of a WHILE statement.
6. class *Until_stmt* - stores a condition and a code_block of an UNTIL statement.
7. class *Assign* - stores the left and right values of an assignment operator 'op' and the operator itself.
8. class *Boolean_stmt* - stores the left and right values of a relational operator 'REL_op' and the operator itself.
9. class *Puts* - stores the value to be printed.
10. class *Var* - stores the ID(Identifier) Token and its value.
11. class *Num* - stores the Integer token and its value.
12. class *Compound* - stroes a list of statements.
13. class *NoOP* - an empty class.

### **Class Parser** 

It parses the given string of input to an abstract syntax tree. It has the following functions:

***__init__*** - 

a constuctor to create a parse object and store Lexer object and current token.

***error*** - 

raises an exception called "Invalid Syntax".

***eat*** - 

checks if the current token type is of the desired token type, if it is not then calls the ***error*** function.

***factor*** - 

It parses the string according to the BNF : ' factor : INTEGER | LPAREN expr RPAREN | variable|string ' and returns either a value returned by ***string*** function or Num(Integer token) object or value returned by ***expr*** function or value returned by ***variable*** function.

***term*** -

It parses the string according to the BNF : ' term : factor ((MUL | DIV) factor)\* ' It stores the value returned by ***factor*** function in node variable and if next token is either 'MUL' token or 'DIV' token then returns an object BinOp(left=node, op=token, right=self.factor()) else it just return the node variable previously created.

***expr*** - 

It parses the string according to the BNF :  expr   : ' term ((PLUS | MINUS) term)/* '.It stores the value returned by ***term*** function in node variable and if next token is either 'PLUS' token or 'MINUS' token then returns an object BinOp(left=node, op=token, right=self.term()) else it just return the node variable previously created.

The above three functions are used to parse plus,minus,multipy,divide operations on the given variables or Integers according to the precedence multiply,divide greater than +,-.

***bol_expr*** - 

# Interpreter

It has different classes to get the abstract syntax tree from parser and analyses it using semantics of ruby language. It imports both [*parser*] (#parser) and [*lexer*] (#lexer).

Different classes used in this are :
1. Node Visitor : Visits the nodes of abstract syntax tree
2. Interpreter.
3. Main.
## Node Visitor 
***visit*** -

visits the nodes of the AST and returns its value.

***generic_visit*** - 

raises error message for invalid node entry.

## Class Interpreter 

contains the following functions/methods:

***__init__*** - 

a contructor which creates AST from parse object.

***visit_String*** -

returns node value.

***visit_BinOp*** -

checks for binary operators such as plus, minus, multplication and division.
Returns the compound value of node.left (bin_op) node.right.

***visit_Boolean_stmt*** -

checks for boolean statements and again returns the final boolean value based on node.left and node.right.

***visit_If_stmt*** -

if the condition is true it returns the codeblock corresponding to if statement, else it will return the codeblock corresponding to else block.

***visit_Unless_stmt*** -

returns the codeblock unless the bool condition becomes false.

***visit_While_stmt*** -

if condition is true visits the codeblock and then returns the while node.

***visit_Until_stmt*** -

if condition is false visits the codeblock and then returns the while node.

***visit_Num*** -

returs the numerical value of the node.

***visit_Puts*** -

activates when puts keyword is encountered. It will print the statement/value after it.

***interpret*** -
interprest the AST and returns the fial output.

## main 
Takes input from ruby file. Which then form the part of the following code,
```
lexer = Lexer(text)
parser = Parser(lexer)
interpreter = Interpreter(parser)
result = interpreter.interpret()
```

# Contributors - 
1. ANDALURI S P V M ADITYA - CS21B002
2. A SHREE BALAJI- CS21B008
3. CHETAN MOTURI- CS21B017
4. K E NANDA KISHORE- CS21B025
5. TEJA MANCHIKATLA- CS21B031.

THANK YOU!!!

