# Simple postfix parser with integers
s = "((((3 4 +) 9 *) (8 9 +) *) 1050 -) 2 ^)"

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

# Convert numbers into integers
number.setParseAction(lambda x:int(x["value"])) 

# Apply a function depending on the symbol
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

result = expr.parseString(s)[0]
print "Final value:", result

