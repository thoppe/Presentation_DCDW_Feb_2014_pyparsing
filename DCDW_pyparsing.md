{"theme":"beige.css"}

# PYPARSING
### _helping data get its sexy back_

*[Travis Hoppe](http://thoppe.github.io/)*
_[DC Data Wranglers](http://www.meetup.com/Data-Wranglers-DC/)_ / [(deck source)](https://github.com/thoppe/DCDW_pres_feb_2014)

====

## What is parsing?

_syntactic analysis of symbols_
_according to a formal grammar_


Analyzing a log file
Extracting data from a webpage
Sanitizing input from untrusted sources

====*

## don't do it!

Write the *grammar* not the *parser*!

It's easier to construct/maintain 
a mini-language. Really!

Traditional utilities: regex, lex, yacc.

====*

## Example problems

### Easy:
Addresses, phone numbers, quoted strings

### Hard:
HTML, recursive descent parsers
(mathematical expressions, pdf's, meta-font, LISP)

====

## Lifecycle of code

+ Time to code
+ Time to run
+ Time to maintain


_Which is more important?_

====*

This is not NLP (natural language processing)
This is a *context-free* grammar.


====+
<br>

### One morning I shot an elephant in my pajamas. 
====+
### How he got into my pajamas I'll never know.
_(sometimes context matters!)_

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

"_Regular expressions are like a particularly spicy hot sauce, to be used in moderation and with restraint only when appropriate. If you drench your plate in hot sauce, you're going to be very, very sorry later._" - Jeff Atwood

====*

Validating a phone number (_reasonable regex_)
    "^\(*\d{3}\)*( |-)*\d{3}( |-)*\d{4}$"

Validating RFC822 email addresses (_have fun!_)
{"include_code":"code/badregex.txt"}

====
# Pyparsing
A free, pure python drop-in [parsing module](http://pyparsing.wikispaces.com/). Allows you to write/maintain the grammar, _abstracted_ from the parser.
!(images/book.jpg)[http://shop.oreilly.com/product/9780596514235.do]<<height:300px>>
 Examples in this talk adapted from the [book](http://shop.oreilly.com/product/9780596514235.do).

====
### [hello_world.py](code/hello_world.py)
Build the grammar iteratively, bottom up
    from pyparsing import *
    s = "Hello World!"
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

Like OOP, each mini-grammar can be reused
    s2 = "Hello sir, how are you today?"
    phrase  = Group(word_list) + (Literal(",") | end_punc).suppress()
    grammar = OneOrMore(phrase)
    print grammar.parseString(s2)

====+

    # [['Hello', 'sir'], ['how', 'are', 'you', 'today']]
	
====
### [records.py](code/records.py)
Take the raw data with missing values
    sue
    Travis Hoppe 31
    Marky Mark 42
    	
    James earl JONES 
    Rudolfo Alphonzo Raffaelo Pierre di Valentina D'Antonguolla 31

====+

and transform it into a nicely type-casted JSON
    [{ "age": null, "name": "Sue"}, 
     { "age": 31,   "name": "Travis Hoppe"}, 
     { "age": 42,   "name": "Marky Mark"}, 
     { "age": null, "name": "James Earl Jones"}, 
     { "age": 31,   "name": "Rudolfo Alphonzo Raffaelo Pierre Di Valentina D'Antonguolla" }]

====*
### [records.py](code/records.py)
The data guides the grammar
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
Our first attempt gives
    print record_list.parseString(data)
    # [['sue'], ['Travis', 'Hoppe'], '31', ['Marky', 'Mark'], '42', ['James', 'earl', 'JONES'], ['Rudolfo', 'Alphonzo', 'Raffaelo', 'Pierre', 'di', 'Valentina', "D'Antonguolla"], '31']

Format the results
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
Proper type casting, string formatting, and a dictionary!
    sol = record_list.parseString(data)
    print sol    	
    # [{'age': None, 'name': 'Sue'}, {'age': 31, 'name': 'Travis Hoppe'}, {'age': 42, 'name': 'Marky Mark'}, {'age': None, 'name': 'James Earl Jones'}, {'age': 31, 'name': "Rudolfo Alphonzo Raffaelo Pierre Di Valentina D'Antonguolla"}]

Pretty-print the results in JSON
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
	expr = Forward()
	LP,RP = map(Suppress, "()")
	expr << (argument | Group(LP + ZeroOrMore(expr) + RP))
	
	print expr.parseString(raw)	
	# [['defun', 'factorial', ['x'], ['if', ['zerop', 'x'], '1', ['*', 'x', ['factorial', ['-', 'x', '1']]]]]]

====
### [postfix_calc.py](code/postfix_calc.py)
Evaluate the string as a mathematical expression
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
### [postfix_calc.py](code/postfix_calc.py)
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
        return val
	
    expr.setParseAction(apply)

====*
### [postfix_calc.py](code/postfix_calc.py)
	s = "((((3 4 +) 9 *) (8 9 +) *) 1050 -) 2 ^)"

Parse results, remove from last group
	result = expr.parseString(s)[0]
	print "Final value:", result

Print statements help debug (use [logging](http://docs.python.org/2/library/logging.html)!)
	Evaluating 3 + 4 = 7
	Evaluating 7 * 9 = 63
	Evaluating 8 + 9 = 17
	Evaluating 63 * 17 = 1071
	Evaluating 1071 - 1050 = 21
	Evaluating 21 ^ 2 = 441
	Final value: 441

====*

### [postfix_calc.py](code/postfix_calc.py)

Extending the functionality is easy!

	actions["%"]      = lambda a,b: a%b
	actions["choose"] = scipy.misc.comb


With a little work, we could make use of unary operators, 
arbitrary length inputs, and floats!

====

###	Why pyparsing?
Grammar specification is a natural-looking part of the python
Class/function names are easier than specialized typography
Easy-to-read and familiar in style
Processing _during_ parsing
Whitespace is _optional_

====+

<br>
### Why not?
Slow for complex grammars (memoization helps)
Specialized libraries may be better (xml, html)
_Sometimes_ overkill (`str.split`?)


====

# Thanks, you.

====*

|## How were these slides made?

###|Math Rendering: $\text{\LaTeX}$
###|JavaScript    : [reveal.js](http://hakim.se/projects/reveal-js)
###|Markdown      : [Daring Fireball](http://daringfireball.net/)

----

###|Markdown to HTML: [md2reveal.py](https://github.com/thoppe/md2reveal)
|_ (uses pyparsing to write a talk about pyparsing)_

====*

## How does it work?

A *text-based* human-readable markup.
SVG equations $e^{i \pi} = -1$, and [links](http://thoppe.github.io/)!
The code for _this particular slide_ looks like this:

    ## How does it work?
    
    A *text-based* human-readable markup. 
    Equation rendering is simple $e^{i \pi} = -1$.
    and [links](http://thoppe.github.io/)!
    The code for this _particular slide_ looks like this:
