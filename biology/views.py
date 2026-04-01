from django.shortcuts import render, get_object_or_404
from .models import Lesson

def lesson_detail(request, lesson_id):
    """Страница с видеоуроком"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'biology/lesson_detail.html', {'lesson': lesson})

def lesson_quiz(request, lesson_id):
    """Страница квиза с автопроверкой"""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.flashcards.all()
    score = None

    if request.method == "POST":
        correct_answers = 0
        for q in questions:
            # Получаем ответ пользователя из формы по ID вопроса
            user_answer = request.POST.get(str(q.id), "").strip().lower()
            correct_answer = q.answer.strip().lower()
            if user_answer == correct_answer:
                correct_answers += 1
        score = f"Вы набрали {correct_answers} из {questions.count()}!"

    return render(request, 'biology/quiz.html', {'lesson': lesson, 'questions': questions, 'score': score})
