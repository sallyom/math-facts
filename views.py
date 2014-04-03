﻿from __future__ import division
from __future__ import unicode_literals

import random

from django.shortcuts import redirect
from django.shortcuts import render

from models import *

magnitude_min = 0
magnitude_max = 12

def get_magnitude(request):
    try:
        return int(request.session['magnitude'])
    except:
        return magnitude_max
    return request.session.get('magnitude', magnitude_max)

## ------------------------------------------------------ ##
    
def index(request):
    context = {}
    template = 'math/index.html'
    return render(request, template, context)


def change_magnitude(request, magnitude=None):
    if magnitude:
        request.session['magnitude'] = magnitude
        next = request.GET.get('next', 'index')
        return redirect(next)
    else:
        current_magnitude = get_magnitude(request)
        magnitude_range = range(magnitude_min, magnitude_max + 1)
        context = { 
            'current_magnitude': current_magnitude,
            'magnitude_range': magnitude_range, 
            'next': request.META['HTTP_REFERER'],
        }
        template = 'math/change_magnitude.html'
        return render(request, template, context)
    
    
def show_facts(request, magnitude=None):
    magnitude = get_magnitude(request)
    terms = range(0, magnitude + 1)

    facts = []
    for term1 in terms:
        for term2 in range(term1 + 1):
            facts.append((term1, term2, term1 + term2))
            
    context = { 
        'magnitude': magnitude, 
        'facts': facts, 
    }
    template = 'math/show_facts.html'
    return render(request, template, context)

    
def show_table(request, magnitude=None):
    magnitude = get_magnitude(request)
    terms = range(0, magnitude + 1)

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
        'magnitude': magnitude, 
        'table': table, 
    }
    template = 'math/show_table.html'
    return render(request, template, context)
        
        
def show_flashcard(request, magnitude=None):
    magnitude = get_magnitude(request)
    
    flashcard = {
        'term1': random.choice(range(magnitude + 1)), 
        'term2': random.choice(range(magnitude + 1)), 
        'operation': '+',
    }
    
    context = {
        'session': request.session,
    }
    context.update(flashcard)
    template = 'math/show_flashcard.html'
    return render(request, template, context)

        
def post_flashcard(request):
    try:
        term1, operation, term2 = request.POST.get('expression').split()
    except:
        return redirect('show_flashcard')
        
    try:
        answer = int(request.POST.get('answer'))
    except: 
        answer = None

    term1 = int(term1)
    term2 = int(term2)
    if operation in  ['+']:
        solution = term1 + term2
    elif operation in ['-', '−', '\u2212']:
        solution = term1 - term2
    elif operation in ['×', '*', '\u00D7']:
        solution = term1 * term2
    elif operation in ['/', '÷', '\u00F7']:
        solution = int(term1 / term2) # may have to do something special here
    else:
        solution = None
        
    success = ( answer == solution )

    # increment cookie ...
    
    nbr_attempts = request.session.get('nbr_attempts', 0) + 1
    nbr_correct = request.session.get('nbr_correct', 0) + success
    
    request.session['nbr_attempts'] = nbr_attempts
    request.session['nbr_correct'] = nbr_correct
    
    context = {
        'session': request.session,
        'term1': term1,
        'term2': term2,
        'operation': operation,
        'solution': solution,
        'answer': answer,
        'success': success,
    }
    template = 'math/post_flashcard.html'
    return render(request, template, context)
   
   
def reset_flashcard_stats(request):
    request.session['nbr_attempts'] = 0
    request.session['nbr_correct'] = 0
    return redirect('show_flashcard')