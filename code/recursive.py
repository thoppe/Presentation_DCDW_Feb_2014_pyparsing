raw ='''(defun factorial (x)
(if (zerop x) 1
(* x (factorial (- x 1)))))'''

from pyparsing import *

expr  = Forward()
alpha = Word(alphas)
operation = oneOf("+ * - /")
number = Word(nums)
argument = alpha | number | operation

LP, RP = Literal("(").suppress(), Literal(")").suppress()
exp << (argument | Group(LP + ZeroOrMore(expr) + RP))

print expr.parseString(raw)




