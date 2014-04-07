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
        maxterm = int(session['maxterm'])
    except:
        maxterm = maxterm_default
    if 'maxterm' not in session:
        session['maxterm'] = maxterm

    operation = session.get('operation', operation_default)
    if 'operation' not in session:
        session['operation'] = operation

    return maxterm, operation

## ------------------------------------------------------ ##

def index(request):
    context = {}
    template = 'math/index.html'
    return render(request, template, context)


def control_panel(request):
    session = request.session
    maxterm, operation = get_controls(session)

    context = {
        'current_maxterm': maxterm,
        'maxterm_range': maxterm_range,
        'current_operation': operation,
        'operation_list': operation_list,
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

    return redirect('control_panel')


def show_flashcard(request):
    session = request.session

    # just a hack until i set up auth/login, etc...
    if 'flashcard_list' not in session:
        flashcard_list = list()
        for expression in initial_expressions_list:
            flashcard_list.append(get_flashcard(expression))
        request.session['flashcard_list'] = flashcard_list
    # end hack

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
        flashcard_list = session.get('flashcard_list', [])
        if flashcard_list:
            flashcard = random.choice(flashcard_list)
        else:
            maxterm, operation = get_controls(session)
            term1 = random.choice(range(maxterm + 1))
            term2 = random.choice(range(maxterm + 1))
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
        expressions_list = request.POST['flashcard_list'].splitlines()
        flashcard_list = list()
        for expression in expressions_list:
            flashcard = get_flashcard(expression)
            if flashcard:
                flashcard_list.append(flashcard)
            else: # there is a problem...
                flashcard_list = request.session.get('flashcard_list', [])
                context = {
                    'error_dump': request.POST['flashcard_list'],
                    'expression': expression,
                }
                template = 'math/edit_flashcard_list.html'
                return render(request, template, context)
        request.session['flashcard_list'] = flashcard_list
    return redirect('control_panel')


def reset_stats(request):
    del request.session['nbr_attempts']
    del request.session['nbr_correct']
    return redirect('show_flashcard')


def list_flashcards(request):
    session = request.session
    maxterm, operation = get_controls(session)
    terms = range(0, maxterm + 1)

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


def show_table(request, maxterm=None):
    session = request.session
    maxterm, operation = get_controls(session)

    if not operation.is_primary:
        operation = operation.inverse

    terms = range(0, maxterm + 1)

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
