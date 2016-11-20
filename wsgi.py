"""
WSGI config for project project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""
from django.contrib.admin import *
from models import *


class FlashcardAttemptAdmin(ModelAdmin):
    def correct(self, obj):
        return obj.is_correct
    correct.boolean = True

    list_display = ['__unicode__', 'correct', 'attempt_at']
    list_filter = ['user', 'attempt_at']

site.register(FlashcardAttempt, FlashcardAttemptAdmin)

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

application = get_wsgi_application()
