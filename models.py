from __future__ import division
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db.models import *

## ------------------------------------------------------ ##

class Operation(object):
    def __init__(self, name, ascii, symbol, inverse_of=None):
        self.name = name
        self.ascii = ascii
        self.symbol = symbol
        self.inverse = inverse_of
        self.is_primary = ( inverse_of == None )

        if inverse_of:
            self.inverse.inverse = self

    def __unicode__(self):
        return self.symbol


add = Operation('addition', '+', '+')
sub = Operation('subtraction', '-' , '−', inverse_of=add)
mul = Operation('multiplication', '*' , '×')
div = Operation('division', '/' , '÷', inverse_of=mul)

operation_list = [add, sub, mul, div]
operation_default = mul

## ------------------------------------------------------ ##

class Flashcard(object):
    def __init__(self, term1, term2, operation):
        self.term1 = int(term1)
        self.term2 = int(term2)
        self.operation = operation

    @property
    def expression(self):
        return '{self.term1}{self.operation.ascii}{self.term2}'.format(self=self)

    @property
    def answer(self):
        try:
            return int(eval(self.expression))
        except:
            return None

    @property
    def inverse(self):
        if self.operation.inverse_of:
            return Flashcard(self.answer, self.term2, self.operation.inverse_of)
        return None

    def __unicode__(self):
        return '{self.term1} {self.operation} {self.term2} = {self.answer}'.format(self=self)

## ------------------------------------------------------ ##

def get_flashcard(expression):
    try:
        for operation in operation_list:
            if operation.ascii in expression:
                term1, term2 = expression.split(operation.ascii)
                break
            elif operation.symbol in expression:
                term1, term2 = expression.split(operation.symbol)
                break
        return Flashcard(term1, term2, operation)
    except:
        return None


def generate_flashcard(term1, term2, operation):
    if not operation.is_primary:
        primary_flashcard = Flashcard(term1, term2, operation.inverse)
        term1 = primary_flashcard.answer
    return Flashcard(term1, term2, operation)

def evaluate_flashcard(flashcard, proposed_answer):
    try:
        proposed_answer = int(proposed_answer)
    except:
        proposed_answer = None
    return ( proposed_answer == flashcard.answer )


## ------------------------------------------------------ ##

maxterm_range = range(13) # this is 0 to 12
maxterm_default = 5

initial_expression_list = []
for i in range(13):
    for j in range(13):
        initial_expression_list.append('{} + {}'.format(i, j))
        initial_expression_list.append('{} - {}'.format(i + j, i))
        
## ------------------------------------------------------ ##

class FlashcardAttempt(Model):
    user = ForeignKey(User)
    expression = CharField(max_length=200)
    attempt = IntegerField(null=True, blank=True)
    attempt_at = DateTimeField(auto_now_add=True)

    @property
    def flashcard(self):
        return get_flashcard(self.expression)

    @property
    def is_correct(self):
        return ( self.attempt == self.flashcard.answer )

    def __unicode__(self):
        return '{self.user} | {self.expression}={self.attempt}'.format(self=self)

    class Meta:
        ordering = ['user', '-attempt_at']
