from __future__ import division
from __future__ import unicode_literals


class Operation(object):
    def __init__(self, name, ascii, symbol, inverse_of=None):
        self.name = name
        self.ascii = ascii
        self.symbol = symbol
        self.inverse_of = inverse_of

add = Operation('addition', '+', '+')
sub = Operation('subtraction', '-' , '−', inverse_of=add),
mul = Operation('multiplication', '*' , '×')
div = Operation('division', '/' , '÷', inverse_of=mul),

operation_list = [add, mul]
operation_default = mul

## ------------------------------------------------------ ##

magnitude_range = range(13) # this is 0 to 12
magnitude_default = 5

class Flashcard(object):
    def __init__(self, expression):
        term1, operation_ascii, term2 = expression.split()

        self.term1 = int(term1)
        self.term2 = int(term2)

        for operation in operation_list:
            if operation.ascii == operation_ascii:
                break
        self.operation = operation

    @property
    def answer(self):
        if self.operation.ascii == '+':
            answer = self.term1 + self.term2
        elif self.operation.ascii == '-':
            answer = self.term1 - self.term2
        elif self.operation.ascii == '*':
            answer = self.term1 * self.term2
        elif self.operation.ascii == '/':
            if self.term2:
                answer = int(self.term1 / self.term2) # may have to do something special here
            else:
                answer = None
        else:
            answer = None
        return answer



mag = 20
ops = ['+-', '*/']

flashcards = {}
for op in ops:
    for term1 in range(mag + 1):
        for term2 in range(mag + 1):
            # create primary flashcard
            expression = ' '.join([str(term1), op[0], str(term2)])
            flashcard = Flashcard(expression)
            flashcards[expression] = flashcard

            # create inverse flashcard
            expression = ' '.join([str(flashcard.answer), op[1], str(term2)])
            flashcard = Flashcard(expression)
            flashcards[expression] = flashcard

