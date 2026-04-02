"""Admin configuration for the biology app."""
from django.contrib import admin
from .models import Lesson, Flashcard, UserProgress

admin.site.register(Lesson)
admin.site.register(Flashcard)
admin.site.register(UserProgress)
