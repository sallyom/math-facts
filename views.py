from __future__ import division
from __future__ import unicode_literals

import random

from django.shortcuts import redirect
from django.shortcuts import render

from models import *

magnitude_min = 0
magnitude_max = 12
magnitude_default = 5

def get_magnitude(request):
    try:
        return int(request.session['magnitude'])
    except:
        return magnitude_default
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


def show_flashcard(request, magnitude=None):
    session = request.session
    if 'evaluate' in session:
        del session['evaluate']
        session = request.session
        flashcard = flashcards[session['expression']]

        try:
            proposed_answer = int(session['proposal'])
        except:
            proposed_answer = None

        success = ( proposed_answer == flashcard.answer )

        session['nbr_attempts'] = session.get('nbr_attempts', 0) + 1
        session['nbr_correct'] = session.get('nbr_correct', 0) + success

        context = {
            'term1': flashcard.term1,
            'term2': flashcard.term2,
            'operation': flashcard.operation,
            'answer': flashcard.answer,
            'success': success,
        }
        context.update(session)
        template = 'math/show_flashcard_result.html'
    else:
        magnitude = get_magnitude(request)
        context = {
            'term1': random.choice(range(magnitude + 1)),
            'term2': random.choice(range(magnitude + 1)),
            'operation': '+',
        }
        context.update(session)
        template = 'math/show_flashcard.html'

    return render(request, template, context)


def post_flashcard(request):
    request.session['evaluate'] = True
    request.session['expression'] = request.POST['expression']
    try:
        request.session['proposal'] = int(request.POST['proposal'])
    except:
        request.session['proposal'] = None
    return redirect('show_flashcard')


def reset_flashcard_stats(request):
    del request.session['nbr_attempts']
    del request.session['nbr_correct']
    return redirect('show_flashcard')


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
