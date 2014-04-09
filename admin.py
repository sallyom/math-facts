from django.contrib.admin import *
from models import *


class FlashcardAttemptAdmin(ModelAdmin):
    def correct(self, obj):
        return obj.is_correct
    correct.boolean = True

    list_display = ['__unicode__', 'correct', 'attempt_at']
    list_filter = ['user', 'attempt_at']

site.register(FlashcardAttempt, FlashcardAttemptAdmin)
