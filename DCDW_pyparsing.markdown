{"theme":"beige.css"}

# PYPARSING
### _helping data get its sexy back_

Travis Hoppe
DC *Data Wranglers*

====

## Lifecycle of code

+ Time to code
+ Time to run
+ Time to maintain

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
What is parsing?

> Def of parsing

... don't do it!

====
Write the grammar not the parser!


Write a mini-lanuage - really!

====
This is not NLP (natural lanuage processing)

This is a *context-free* grammar.

### One morning I shot an elephant in my pajamas. 


### How he got into my pajamas I'll never know.

====
# BNF
## Backus–Naur Form

Wikipedia def.

> ... a notation for a context-free grammar, used to describe the syntax of languages used in computing, such as computer programming languages, document formats, instruction sets and communication protocols

====
# Pyarsing

====
## Example problems

### Easy:
Address, phone numbers, quoted strings

### Hard:
HTML, recursive descent parser (mathematical expression, ...), recursive expressions (pdf's, meta-font, LISP)



	
