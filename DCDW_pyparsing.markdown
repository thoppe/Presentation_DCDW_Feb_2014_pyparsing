{"theme":"beige.css"}

# PYPARSING
### _helping data get its sexy back_

*[Travis Hoppe](http://thoppe.github.io/)*
_[DC Data Wranglers](http://www.meetup.com/Data-Wranglers-DC/)_ / [(deck source)](https://github.com/thoppe/DCDW_pres_feb_2014)

====

## What is parsing?

_syntactic analysis of symbols_
_according to a formal gramar_


+ Analying a log file
+ Extracting data from a webpage
+ Sanitizing input from untrusted sources

====*

## don't do it!

Write the *grammar* not the *parser*!

It's easier to construct/maintain 
a mini-lanuage - really!

Traditional utilites: `regex, lex, yacc`

====*

## Example problems

### Easy:
Address, phone numbers, quoted strings

### Hard:
HTML, recursive descent parser (mathematical expressions, pdf's, meta-font, LISP, ...)

====

## Lifecycle of code

+ Time to code
+ Time to run
+ Time to maintain


_Which is more important?_

====*

### This is not NLP (natural lanuage processing)
_A computer scientist and a linguist walk into a bar..._
This is a *context-free* grammar.
<br>
====+
<br>

### One morning I shot an elephant in my pajamas. 
====+
### How he got into my pajamas I'll never know.

====*
# Backus-Naur Form

"_... a notation for a context-free grammar, used to describe the syntax of languages used in computing, such as computer programming languages, document formats, instruction sets and communication protocols_" - Wikipedia
 
    <postal-address> ::= <name-part> <street-address> <zip-part>
    <name-part>      ::= <personal-part> <last-name> <opt-suffix-part> <EOL> 
                       | <personal-part> <name-part>
    <personal-part>  ::= <first-name> | <initial> "." 
    <street-address> ::= <house-num> <street-name> <opt-apt-num> <EOL>
    <zip-part> ::= <town-name> "," <state-code> <ZIP-code> <EOL>

====

## Why not regex?
_[Now you have two problems](http://www.codinghorror.com/blog/2008/06/regular-expressions-now-you-have-two-problems.html)_


> Regular expressions are like a particularly spicy hot sauce – to be used in moderation and with restraint only when appropriate. If you drench your plate in hot sauce, you're going to be very, very sorry later.

====*

Validating a phone number (_reasonable regex_)

    "^\(*\d{3}\)*( |-)*\d{3}( |-)*\d{4}$"

Validating RFC822 email addresses (_have fun!_)

{"include_code":"badregex.txt"}

====
# Pyarsing

Pure python drop-in (free) parsing module with an expressive syntax. Allows you to write/maintain the grammar, _abstracted_ from the parser.
!(book.jpg)[http://shop.oreilly.com/product/9780596514235.do]<<height:300px>>

====
### [hello_world.py](code/hello_world.py)

    from pyparsing import *
    s = "Hello world!"
    word = Word(alphas)
    grammar = word
    print grammar.parseString(s)
    # Only grabs "Hello"
		
====+

    word_list = OneOrMore(word)
    grammar   = word_list
    # Now we get a list ["Hello", "World"]
	
====+

    end_punc = oneOf(". ! ?")
    grammar  = word_list + end_punc
    # Grabs the end symbol ["Hello", "World", "!"]
	
====+

    grammar = Group(word_list) + end_punc.suppress()
    # Group and suppress [["Hello", "World"]]

====*

### [hello_world.py](code/hello_world.py)

    s2 = "Hello sir, how are you today?"
    phrase  = Group(word_list) + (Literal(",") | end_punc).suppress()
    grammar = OneOrMore(phrase)
    print grammar.parseString(s2)

====+

    # [['Hello', 'sir'], ['how', 'are', 'you', 'today']]
	
====
### [records.py](code/records.py)
Objective: Take the raw data with missing values
    sue
    Travis Hoppe 31
    Marky Mark 42
    	
    James earl JONES 
    Rudolfo Alphonzo Raffaelo Pierre di Valentina D'Antonguolla 31

====+

And transform it into a nicely type-casted JSON:
    [{ "age": null, "name": "Sue"}, 
     { "age": 31,   "name": "Travis Hoppe"}, 
     { "age": 42,   "name": "Marky Mark"}, 
     { "age": null, "name": "James Earl Jones"}, 
     { "age": 31, "name": "Rudolfo Alphonzo Raffaelo Pierre Di Valentina D'Antonguolla" }]

====*
### [records.py](code/records.py)
The data guides the grammar:
    sue
    Travis Hoppe 31
    Marky Mark 42
    
    James earl JONES 
    Rudolfo Alphonzo Raffaelo Pierre di Valentina D'Antonguolla 31
and self-documents the process for maintenance
    ParserElement.setDefaultWhitespaceChars(' \t')
    
    name      = Word(alphas + "'")
    full_name = Group(OneOrMore(name))("name")
    age = Word(nums)("age")
    EOL = LineEnd().suppress()
    
    record = full_name + Optional(age) + EOL
    record_list = OneOrMore(record | EOL)

====*
### [records.py](code/records.py)
Our first attempt gives:
    print record_list.parseString(data)
    # [['sue', 'Travis', 'Hoppe'], '31', ['Marky', 'Mark'], '42', ['James', 'earl', 'JONES', 'Rudolfo', 'Alphonzo', 'Raffaelo', 'Pierre', 'di', 'Valentina', "D'Antonguolla"], '31']

Let's format the results:
    def clean_record(tokens):
      name = ' '.join(tokens["name"]).title()
      if "age" in tokens:
          age = int(tokens["age"])
      else:
          age = None
      return {'name':name, 'age':age}
    
    record.setParseAction(clean_record)
	  
====*
### [records.py](code/records.py) 
Proper type casting, string formating and dictionary formating!
    sol = record_list.parseString(data)
    print sol    	
    # [{'age': 31, 'name': 'Sue Travis Hoppe'}, {'age': 42, 'name': 'Marky Mark'}, {'age': 31, 'name': "James Earl Jones Rudolfo Alphonzo Raffaelo Pierre Di Valentina D'Antonguolla"}]

Now pretty-print the results in JSON:
    import json
    js = json.dumps(sol.asList(),indent=2)
    print js
    
    # [{"age": null, "name": "Sue"}, 
    # { "age": 31,   "name": "Travis Hoppe"}, 
    # { "age": 42,   "name": "Marky Mark"}, 
    # { "age": null, "name": "James Earl Jones"}, 
    # { "age": 31, "name": "Rudolfo Alphonzo Raffaelo Pierre Di Valentina D'Antonguolla" }]


====
### [recursive.py](code/recursive.py)
	raw ='''(defun factorial (x)
	(if (zerop x) 1
	(* x (factorial (- x 1)))))'''

====+

	from pyparsing import *
	alpha  = Word(alphas)
	operation = oneOf("+ * - /")
	number = Word(nums)
	argument = alpha | number | operation
	
====+
The expression is a recursive grammar!
	exp = Forward()
	LP, RP = Literal("(").suppress(), Literal(")").suppress()
	exp << (argument | Group(LP + ZeroOrMore(exp) + RP))
	
	print exp.parseString(raw)	
	# [['defun', 'factorial', ['x'], ['if', ['zerop', 'x'], '1', ['*', 'x', ['factorial', ['-', 'x', '1']]]]]]

====
### [prefix_calc.py](code/prefix_calc.py)
Evalute the string as a mathematical expression:
	s = "((((3 4 +) 9 *) (8 9 +) *) 1050 -) 2 ^)"

====+
	from pyparsing import *
	expr = Forward()
	number    = Word(nums)("value")
	operation = oneOf("+ * ^ -")
	LP, RP = Literal("(").suppress(), Literal(")").suppress()
	nest = (LP + expr + RP)
	expr << Group(  (number | nest) 
                  + (number | nest) 
                  + operation)
	
    print expr.parseString(s)
	#[[[[[['3', '4', '+'], '9', '*'], ['8', '9', '+'], '*'], '1050', '-'], '2', '^']]

====*
### [prefix_calc.py](code/prefix_calc.py)
Convert numbers into integers
	number.setParseAction(lambda x:int(x["value"])) 

Apply a function depending on the symbol
	actions = {"+":lambda x,y:x+y,
        "*":lambda x,y:x*y,
		"-":lambda x,y:x-y,
        "^":lambda x,y:x**y}
	
	def apply(tokens):
		a,b,op = tokens[0]
        val = actions[op](a,b)
        print "Evaluating {} {} {} = {}".format(a,op,b,val)
        return actions[op](a,b)
	
    expr.setParseAction(apply)

====*
### [prefix_calc.py](code/prefix_calc.py)
	s = "((((3 4 +) 9 *) (8 9 +) *) 1050 -) 2 ^)"

Parse results, take out of last group
	result = expr.parseString(s)[0]
	print "Final value:", result

Print statements help debug (use [logging](http://docs.python.org/2/library/logging.html) module!)
	Evaluating 3 + 4 = 7
	Evaluating 7 * 9 = 63
	Evaluating 8 + 9 = 17
	Evaluating 63 * 17 = 1071
	Evaluating 1071 - 1050 = 21
	Evaluating 21 ^ 2 = 441
	Final value: 441
