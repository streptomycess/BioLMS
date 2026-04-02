"""Database models for the biology Learning Management System."""
import re
from django.db import models

class Lesson(models.Model):
    """Represents a single biology lesson containing a video."""
    title = models.CharField(max_length=200, verbose_name="Название урока")
    video_url = models.URLField(verbose_name="Ссылка на YouTube")

    @property
    def embed_url(self):
        """Extracts the YouTube ID to create an embeddable URL."""
        match = re.search(r'(?:v=|\/)([0-9A-Za-z_-]{11})', self.video_url)
        if match:
            return f"https://www.youtube.com/embed/{match.group(1)}"
        return self.video_url

    def __str__(self):
        return str(self.title)

class Flashcard(models.Model):
    """Represents a quiz question linked to a specific lesson."""
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="flashcards")
    question = models.CharField(max_length=300, verbose_name="Вопрос")
    answer = models.CharField(max_length=300, verbose_name="Ответ")

    def __str__(self):
        return str(self.question)
