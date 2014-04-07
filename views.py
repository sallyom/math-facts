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

#     if 'next' in request.GET:
#         next = request.GET['next']
#     else:
#         next = request.META.get('HTTP_REFERER', '/')

    context = {
        'current_magnitude': magnitude,
        'magnitude_range': magnitude_range,
        'current_operation': operation,
        'operation_list': operation_list,
#         'next': next,
    }
    context.update(session)
    template = 'math/control_panel.html'
    return render(request, template, context)


def change_controls(request, key, value):
    if key == 'operation':
        for operation in operation_list:
            if operation.name == value:
                break
        value = operation
    request.session[key] = value

#     next = request.GET['next']
    response = redirect('control_panel')
#     response['Location'] += '?next={}'.format(next)
    return response


def show_flashcard(request):
    session = request.session
    if 'evaluate' in session:
        del session['evaluate']
        session = request.session
        flashcard = get_flashcard(session['expression'])

        try:
            proposed_answer = int(session['proposal'])
        except:
            proposed_answer = None

        success = ( proposed_answer == flashcard.answer )

        session['nbr_attempts'] = session.get('nbr_attempts', 0) + 1
        session['nbr_correct'] = session.get('nbr_correct', 0) + success

        context = {
            'flashcard': flashcard,
            'success': success,
        }
        context.update(session)
        template = 'math/show_flashcard_result.html'
    else:
        if 'flashcard_list' in session:
            flashcard = random.choice(session['flashcard_list'])
        else:
            magnitude, operation = get_controls(session)
            term1 = random.choice(range(magnitude + 1))
            term2 = random.choice(range(magnitude + 1))
            flashcard = generate_flashcard(term1, term2, operation)
        context = {
            'flashcard': flashcard,
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


def edit_flashcard_list(request):
    flashcard_list = request.session.get('flashcard_list', [])
    context = {
        'flashcard_list': flashcard_list,
    }
    template = 'math/edit_flashcard_list.html'
    return render(request, template, context)


def post_flashcard_list(request):
    if 'flashcard_list' in request.POST:
        flashcard_list = list()
        expressions_list = request.POST['flashcard_list'].splitlines()
        for expression in expressions_list:
            flashcard_list.append(get_flashcard(expression))
        if flashcard_list:
            request.session['flashcard_list'] = flashcard_list
        else:
            del request.session['flashcard_list']
    return redirect('control_panel')


def reset_stats(request):
    del request.session['nbr_attempts']
    del request.session['nbr_correct']
    return redirect('show_flashcard')


def list_flashcards(request):
    session = request.session
    magnitude, operation = get_controls(session)
    terms = range(0, magnitude + 1)

    flashcard_pairs = []
    for term1 in terms:
        for term2 in range(term1 + 1):
            flashcard1 = generate_flashcard(term1, term2, operation)
            flashcard2 = generate_flashcard(term2, term1, operation)
            flashcard_pairs.append((flashcard1, flashcard2))

    context = {
        'flashcard_pairs': flashcard_pairs,
    }
    context.update(session)
    template = 'math/list_flashcards.html'
    return render(request, template, context)


def show_table(request, magnitude=None):
    session = request.session
    magnitude, operation = get_controls(session)

    if not operation.is_primary:
        operation = operation.inverse

    terms = range(0, magnitude + 1)

    table = {
        'corner': operation,
        'headers': [],
        'rows': [],
    }

    for term1 in terms:
        table['headers'].append(term1)
        facts = []
        for term2 in terms:
            flashcard = generate_flashcard(term1, term2, operation)
            facts.append(flashcard.answer)
        table['rows'].append({ 'term': term1, 'facts': facts })

    context = {
        'table': table,
        'table_operation': operation,
    }
    context.update(session)
    template = 'math/show_table.html'
    return render(request, template, context)
