from pyparsing import *

s = "Hello world!"

word = Word(alphas)
grammar = word
print grammar.parseString(s)
#> hello : Only captures the first word

word_list = OneOrMore(word)
grammar   = word_list
print grammar.parseString(s)
#> [hello, world] : Missing the end symbol

end_punc = oneOf(". ! ?")
grammar  = word_list + end_punc
print grammar.parseString(s)
#> [hello, world], ! : Missing the end symbol

grammar = Group(word_list) + end_punc.suppress()
print grammar.parseString(s)
#> [[hello, world]] : Group the section drops the end_punc

s2 = "Hello sir, how are you today?"
phrase  = Group(word_list) + (Literal(",") | end_punc).suppress()
grammar = OneOrMore(phrase)
print grammar.parseString(s2)

