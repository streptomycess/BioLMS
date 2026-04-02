"""View controllers for handling biology lesson logic and registration."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Lesson

def register(request):
    """Handle new user registration."""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'biology/register.html', {'form': form})

def home(request):
    """Display the list of all available lessons."""
    lessons = Lesson.objects.all()
    return render(request, 'biology/home.html', {'lessons': lessons})

def lesson_detail(request, lesson_id):
    """Show details for a specific lesson."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'biology/lesson_detail.html', {'lesson': lesson})

def lesson_quiz(request, lesson_id):
    """Handle the quiz logic for a specific lesson."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.flashcards.all()
    score = None

    if request.method == "POST":
        correct_answers = 0
        for q in questions:
            user_answer = request.POST.get(str(q.id), "").strip().lower()
            correct_answer = q.answer.strip().lower()
            if user_answer == correct_answer:
                correct_answers += 1
        # Fixed line length by breaking the string
        score = (
            f"Вы набрали {correct_answers} из {questions.count()}!"
        )

    return render(request, 'biology/quiz.html', {
        'lesson': lesson,
        'questions': questions,
        'score': score
    })
