from __future__ import division
from __future__ import unicode_literals

class Flashcard(object):
    def __init__(self, expression):
        term1, operation, term2 = expression.split()

        self.term1 = int(term1)
        self.term2 = int(term2)

        if operation in  ['+']:
            self.operation = '+'
        elif operation in ['-', '−', '\u2212']:
            self.operation = '-'
        elif operation in ['×', '*', '\u00D7']:
            self.operation = '*'
        elif operation in ['/', '÷', '\u00F7']:
            self.operation = '/'
        
    @property
    def answer(self):
        if self.operation == '+':
            answer = self.term1 + self.term2
        elif self.operation == '-':
            answer = self.term1 - self.term2
        elif self.operation == '*':
            answer = self.term1 * self.term2
        elif self.operation == '/': 
            answer = int(self.term1 / self.term2) # may have to do something special here
        else:
            answer = None
        return answer

magnitude = 5
operations = ['+-', '*/']

flashcards = {}
for operation in operations:
    for term1 in range(magnitude + 1):
        for term2 in range(magnitude + 1):
            # create primary flashcard
            expression = ' '.join([str(term1), operation[0], str(term2)])
            flashcard = Flashcard(expression)
            flashcards[expression] = flashcard
            
            # create inverse flashcard
            expression = ' '.join([str(flashcard.answer), operation[1], str(term2)])
            flashcard = Flashcard(expression)
            flashcards[expression] = flashcard
            
