from __future__ import division
from __future__ import unicode_literals


class Operation(object):
    def __init__(self, name, ascii, symbol, inverse_of=None):
        self.name = name
        self.ascii = ascii
        self.symbol = symbol
        self.inverse = inverse_of
        self.is_primary = ( inverse_of == None )

        if inverse_of:
            self.inverse.inverse = self


add = Operation('addition', '+', '+')
sub = Operation('subtraction', '-' , '−', inverse_of=add)
mul = Operation('multiplication', '*' , '×')
div = Operation('division', '/' , '÷', inverse_of=mul)

operation_list = [add, sub, mul, div]
operation_default = mul

## ------------------------------------------------------ ##

magnitude_range = range(13) # this is 0 to 12
magnitude_default = 5

class Flashcard(object):
    def __init__(self, term1, term2, operation):
        self.term1 = int(term1)
        self.term2 = int(term2)
        self.operation = operation

    @property
    def expression(self):
        return ' '.join([self.term1, self.operation.ascii, self.term2])

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

    @property
    def inverse(self):
        if self.operation.inverse_of:
            return Flashcard(self.answer, self.term2, self.operation.inverse_of)
        return None


# mag = 20
#
# flashcards = {}
# for operation in operation_list:
#     for term1 in range(mag + 1):
#         for term2 in range(mag + 1):
#             # create primary flashcard
#             expression = ' '.join([str(term1), op[0], str(term2)])
#             flashcard = Flashcard(expression)
#             flashcards[expression] = flashcard
#
#             # create inverse flashcard
#             expression = ' '.join([str(flashcard.answer), op[1], str(term2)])
#             flashcard = Flashcard(expression)
#             flashcards[expression] = flashcard
#
