from __future__ import division
from __future__ import unicode_literals

magnitude_range = range(13) # this is 0 to 12
magnitude_default = 5

operation_list = [
    { 'ascii': '+', 'display': '+', 'name': 'addition'       },
#     { 'ascii': '-', 'display': '−', 'name': 'subration'      },
    { 'ascii': '*', 'display': '×', 'name': 'multiplication' },
#     { 'ascii': '/', 'display': '÷', 'name': 'division'       },
]

operation_default = operation_list[1]

# class Operation(object):
#     objects = []
#
#     def __init(self, symbol, display, name):
#         self.symbol = symbol
#         self.display = display
#         self.name = name
#
# operation_list = [
#     Operation('+', '+', 'addition'      ),
#     Operation('-', '−', 'subtraction'   ),
#     Operation('*', '×', 'multiplication'),
#     Operation('/', '÷', 'division'      ),
# ]

## ------------------------------------------------------ ##

class Flashcard(object):
    def __init__(self, expression):
        term1, operation_ascii, term2 = expression.split()

        self.term1 = int(term1)
        self.term2 = int(term2)

        for operation in operation_list:
            if operation['ascii'] == operation_ascii:
                break
        self.operation = operation

        if operation['ascii'] == '+':
            self.answer = self.term1 + self.term2
        elif operation['ascii'] == '-':
            self.answer = self.term1 - self.term2
        elif operation['ascii'] == '*':
            self.answer = self.term1 * self.term2
        elif operation['ascii'] == '/':
            if self.term2:
                self.answer = int(self.term1 / self.term2) # may have to do something special here
            else:
                self.answer = None
        else:
            self.answer = None


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

