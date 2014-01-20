from pyparsing import *

data = '''sue
Travis Hoppe 31
Marky Mark 42

James earl JONES 
Rudolfo Alphonzo Raffaelo Pierre di Valentina D'Antonguolla 31
'''

ParserElement.setDefaultWhitespaceChars(' \t')

name      = Word(alphas + "'")
full_name = Group(OneOrMore(name))("name")
age = Word(nums)("age")
EOL = LineEnd().suppress()

record = full_name + Optional(age) + EOL
record_list = OneOrMore(record | EOL)

# First attempt
print record_list.parseString(data)
print

def clean_record(tokens):
    name = ' '.join(tokens["name"]).title()
    if "age" in tokens:
        age = int(tokens["age"])
    else:
        age = None

    return {'name':name, 'age':age}

#def clean_list(tokens):
#    print "HI", tokens
    

record.setParseAction(clean_record)
#record_list.setParseAction(clean_list)

# Now try with the parse actions
sol = record_list.parseString(data)
print sol
print

# Now pretty-print the results in JSON!
import json
js = json.dumps(sol.asList(),indent=2)
print js
