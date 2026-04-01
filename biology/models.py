from django.db import models

class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="Название урока")
    video_url = models.URLField(verbose_name="Ссылка на YouTube")

    @property
    def embed_url(self):
        # Превращаем обычную ссылку в ссылку для встраивания плеера
        return self.video_url.replace("watch?v=", "embed/")

    def __str__(self):
        return self.title

class Flashcard(models.Model):
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="flashcards")
    question = models.CharField(max_length=300, verbose_name="Вопрос")
    answer = models.CharField(max_length=300, verbose_name="Ответ")

    def __str__(self):
        return self.question
