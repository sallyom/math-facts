from __future__ import division
from __future__ import unicode_literals

import random

from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.shortcuts import render

from models import *

## ------------------------------------------------------ ##

def get_controls(session):
    try:
        magnitude = int(session['magnitude'])
    except:
        magnitude = magnitude_default
    if 'magnitude' not in session:
        session['magnitude'] = magnitude

    operation = session.get('operation', operation_default)
    if 'operation' not in session:
        session['operation'] = operation

    return magnitude, operation

## ------------------------------------------------------ ##

def index(request):
    context = {}
    template = 'math/index.html'
    return render(request, template, context)


def control_panel(request):
    session = request.session
    magnitude, operation = get_controls(session)

    if 'next' in request.GET:
        next = request.GET['next']
    else:
        next = request.META.get('HTTP_REFERER', '/')

    context = {
        'current_magnitude': magnitude,
        'magnitude_range': magnitude_range,
        'current_operation': operation,
        'operation_list': operation_list,
        'next': next,
    }
    template = 'math/control_panel.html'
    return render(request, template, context)


def change_controls(request, key, value):
    if key == 'operation':
        for operation in operation_list:
            if operation.name == value:
                break
        value = operation
    request.session[key] = value

    next = request.GET['next']
    response = redirect('control_panel')
    response['Location'] += '?next={}'.format(next)
    return response


def show_flashcard(request):
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
        magnitude, operation = get_controls(session)
        context = {
            'term1': random.choice(range(magnitude + 1)),
            'term2': random.choice(range(magnitude + 1)),
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


def reset_stats(request):
    del request.session['nbr_attempts']
    del request.session['nbr_correct']
    return redirect('show_flashcard')


def show_facts(request):
    session = request.session
    magnitude, operation = get_controls(session)
    terms = range(0, magnitude + 1)

    facts = []
    for term1 in terms:
        for term2 in range(term1 + 1):
            expression = ' '.join([term1, operation, term2])
            flashcard = flashcards(expression)
            facts.append(flashcard)

    context = {
        'facts': facts,
    }
    context.update(session)
    template = 'math/show_facts.html'
    return render(request, template, context)


def show_table(request, magnitude=None):
    session = request.session
    magnitude, operation = get_controls(session)
    terms = range(0, magnitude + 1)

    table = {
        'corner': operation.symbol,
        'headers': [],
        'rows': [],
    }

    for term1 in terms:
        table['headers'].append(term1)
        facts = []
        for term2 in terms:
            expression = ' '.join([term1, operation, term2])
            flashcard = flashcards(expression)
            facts.append(flashcard.answer)
        table['rows'].append({ 'term': term1, 'facts': facts })

    context = {
        'table': table,
    }
    context.update(session)
    template = 'math/show_table.html'
    return render(request, template, context)
