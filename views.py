from __future__ import division
from __future__ import unicode_literals

from django.shortcuts import render

from models import *

def index(request):
    lowest = 3
    highest = 12
    
    context = { 'range': range(lowest, highest + 1) }
    template = 'math/index.html'
    return render(request, template, context)

    
def facts(request, lvl):
    level = int(lvl)

    facts = []
    for a in range(level + 1):
        b = level
        facts.append((a, b, a + b))
            
    context = { 'facts': facts }
    template = 'math/show_facts.html'
    return render(request, template, context)
