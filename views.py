from __future__ import division
from __future__ import unicode_literals

from django.shortcuts import render

from models import *

order_min = 0
order_max = 12

def index(request):
    context = {}
    template = 'math/index.html'
    return render(request, template, context)

    
def show_facts(request, order=None):
    if not order:
        context = { 'range': range(order_min, order_max + 1) }
        template = 'math/list_facts.html'
        return render(request, template, context)
    else:
        order = int(order)
        terms = range(0, order + 1)

        facts = []
        for term1 in terms:
            for term2 in range(term1 + 1):
                facts.append((term1, term2, term1 + term2))
                
        context = { 
            'order': order, 
            'facts': facts, 
        }
        template = 'math/show_facts.html'
        return render(request, template, context)

    
def show_table(request, order=None):
    if not order:
        context = { 'range': range(order_min, order_max + 1) }
        template = 'math/list_tables.html'
        return render(request, template, context)
    else:
        order = int(order)
        terms = range(0, order + 1)

        table = { 
            'corner': '+', 
            'headers': [],
            'rows': [],
        }

        for term1 in terms:
            table['headers'].append(term1)
            sums = []
            for term2 in terms:
                sums.append(term1 + term2)
            table['rows'].append({ 'term': term1, 'sums': sums })
        
        context = { 
            'order': order, 
            'table': table, 
        }
        template = 'math/show_table.html'
        return render(request, template, context)