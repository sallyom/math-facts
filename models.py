﻿from __future__ import division
from __future__ import unicode_literals

from django.utils.safestring import mark_safe


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

magnitude_range = range(13) # this is 0 to 12
magnitude_default = 5

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

    def __unicode__(self):
        return '{self.term1} {self.operation} {self.term2} = {self.answer}'.format(self=self)


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
