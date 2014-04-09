from __future__ import division
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

expression_collection = [
['1+2','0+0','2+2','4+0','1+2','2+3','0+1','3+1','4+1','0+2','1+1','0+5','1+4','3+2','1+0','3+0',],
['2+2','5+0','0+5','3+0','4+1','3+2','1+1','4+0','2+1','0+4','0+1','2+0','1+2','0+0','1+4','2+3',],
['4+0','5+0','3+1','3+0','1+4','3+2','2+2','0+5','0+2','0+3','0+1','0+0','1+2','2+0','4+1','1+3',],
['5-0','5-1','1-0','2-2','3-0','4-1','2-1','4-2','2-0','4-4','3-1','0-0','4-0','4-3','3-2','3-3',],
['5-2','5-4','4-0','5-1','2-1','3-2','4-1','1-1','5-3','0-0','5-0','4-3','3-1','2-0','4-4','3-3',],
['5-2','5-4','4-2','3-0','2-2','1-0','5-1','3-2','4-2','4-4','5-0','5-3','4-1','1-0','3-0','5-4',],
['5-1','1+3','0+5','2+3','5-2','4+1','3+0','4-2','1+2','3-3','2-1','1+3','2+1','2-2','3+2','5-4',],
['8+1','2+7','4+6','7+3','6+1','5+2','7+0','2+6','5+1','6+0','5+3','7+1','5+4','6+3','5+5','0+8',],
['8+2','9+1','6+2','0+7','6+4','5+3','0+6','5+5','10+0','9+0','2+5','1+7','1+6','5+4','7+2','1+8',],
['9+0','8+2','8+0','9+1','10+0','1+5','2+6','8+1','5+5','7+1','6+3','4+5','6+0','7+0','3+7','5+2',],
['8-0','6-1','7-2','7-7','6-2','7-6','6-3','7-1','6-0','7-5','7-0','6-5','6-6','7-4','7-3','6-4',],
['9-7','8-4','9-2','8-8','9-3','9-0','8-5','8-1','9-6','8-3','9-5','8-2','8-7','9-4','8-6','9-1',],
['10-8','9-9','10-2','10-5','9-3','10-3','7-5','10-7','8-6','10-6','6-5','10-1','8-3','10-4','10-9','10-10',],
['10-9','9+1','5+2','8-3','6+4','10-3','7-5','7+0','7-6','10-7','6+3','9-1','6-3','8+2','5+4','8+1',],
['2+9','5+7','6+8','10+5','5+6','10+2','4+7','5+8','6+9','4+9','3+8','5+9','10+4','3+9','4+8','10+3',],
['8+5','7+8','6+6','8+3','9+4','7+5','9+5','8+4','7+7','9+6','6+7','7+4','8+6','8+7','6+6','6+5',],
['10+1','9+3','5+8','3+8','6+6','9+5','10+5','5+7','4+9','5+6','8+6','10+4','9+2','4+7','10+2','7+6',],
['15-9','12-6','14-8','11-5','13-9','11-9','15-6','13-5','11-4','14-9','12-3','14-7','15-8','12-9','11-7','13-4',],
['14-6','11-6','13-8','15-7','11-8','12-4','14-5','12-8','13-7','12-5','13-6','12-7','15-9','14-7','13-7','13-9',],
['12-9','11-4','13-4','15-6','14-6','15-8','14-5','14-8','12-8','13-5','11-7','15-7','14-9','11-9','12-6','13-8',],
['5+9','12-4','6+6','10+3','14-9','15-6','8+4','6+7','11-8','15-7','10+7','13-7','8+3','5+8','12-6','13-4',],
['10+6','8+9','7+9','10+8','8+8','8+10','10+7','9+8','9+9','7+10','10+10','9+7','10+9','6+10','8+9','10+9',],
['10+9','9+7','7+10','10+6','8+9','9+10','9+9','10+10','7+9','10+8','8+8','8+10','10+7','9+8','6+10','10+9',],
['16-9','18-9','17-9','16-7','16-8','17-8','15-6','14-8','20-10','16-8','14-5','18-9','16-9','15-9','17-9','15-8',],
['16-8','15-8','16-9','20-10','18-9','14-5','17-9','15-9','14-8','15-6','17-8','16-7','15-8','20-10','16-9','14-8',],
['9+7','15-6','16-8','10+10','14-8','10+7','9+9','15-7','8+8','16-9','17-9','8+9','20-10','10+6','7+9','14-7',],
]

initial_expressions_list = expression_collection[12]
