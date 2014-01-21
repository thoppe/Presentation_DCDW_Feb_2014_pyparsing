{"theme":"beige.css"}

# PYPARSING
### _helping data get its sexy back_

*[Travis Hoppe](http://thoppe.github.io/)*
_[DC Data Wranglers](http://www.meetup.com/Data-Wranglers-DC/)_

====

## What is parsing?

_syntactic analysis of symbols_
_according to a formal gramar_


+ Analying a log file
+ Extracting data from a webpage
+ Sanatzing input from untrusted sources

====

## don't do it!

Write the *grammar* not the *parser*!

It's easier to construct/maintain 
a mini-lanuage - really!

Traditional utilites include `regex, lex, yacc`

====
## Lifecycle of code

+ Time to code
+ Time to run
+ Time to maintain


_Which is more important?_

====

### This is not NLP (natural lanuage processing)
_A computer scientist and a linguist walk into a bar..._
This is a *context-free* grammar.



### One morning I shot an elephant in my pajamas. 
### How he got into my pajamas I'll never know.

====
# Backus-Naur Form


"_... a notation for a context-free grammar, used to describe the syntax of languages used in computing, such as computer programming languages, document formats, instruction sets and communication protocols_" - Wikipedia

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

Pure python drop-in (free) parsing module with an expressive syntax. 
Allows you to write/maintain the grammar, _abstracted_ from the parser.
!(book.jpg)[http://shop.oreilly.com/product/9780596514235.do]<<height:300px>>


====
## Example problems

### Easy:
Address, phone numbers, quoted strings

### Hard:
HTML, recursive descent parser (mathematical expression, ...), recursive expressions (pdf's, meta-font, LISP)

====
Examples
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
    print grammar.parseString(s)
    # Now we get the list ["Hello", "World"]

====
### [records.py](code/records.py)
====
### [recursive.py](code/recursive.py)
	
