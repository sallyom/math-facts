from __future__ import division
from __future__ import unicode_literals

from django.shortcuts import render

from models import *

def index(request):
    context = { 'text': 'Hello world! $$E = mc^2$$' }
    template = 'math/index.html'
    return render(request, template, context)
