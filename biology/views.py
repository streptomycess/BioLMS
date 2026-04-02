"""View controllers for handling biology lesson logic and registration."""
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .models import Lesson, UserProgress

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
    """Handle the quiz logic for a specific lesson and track user progress."""
    lesson = get_object_or_404(Lesson, id=lesson_id)
    questions = lesson.flashcards.all()
    score = None

    if request.method == "POST":
        correct_answers = 0
        total_questions = questions.count()
        for q in questions:
            user_answer = request.POST.get(str(q.id), "").strip().lower()
            correct_answer = q.answer.strip().lower()
            if user_answer == correct_answer:
                correct_answers += 1

        if request.user.is_authenticated:
            progress, created = UserProgress.objects.get_or_create(
                user=request.user,
                lesson=lesson,
                defaults={'score': correct_answers, 'total': total_questions}
            )
            if not created and correct_answers > progress.score:
                progress.score = correct_answers
                progress.total = total_questions
                progress.save()

        score = f"Вы набрали {correct_answers} из {total_questions}!"

    return render(request, 'biology/quiz.html', {
        'lesson': lesson,
        'questions': questions,
        'score': score
    })

@login_required
def statistics(request):
    """Calculate and display user statistics for individual lessons and overall course progress."""
    progress_records = UserProgress.objects.filter(user=request.user)
    total_lessons = Lesson.objects.count()
    completed_lessons = progress_records.count()

    total_score = sum(p.score for p in progress_records)
    total_possible = sum(p.total for p in progress_records)

    overall_accuracy = 0
    if total_possible > 0:
        overall_accuracy = int((total_score / total_possible) * 100)

    course_completion = 0
    if total_lessons > 0:
        course_completion = int((completed_lessons / total_lessons) * 100)

    return render(request, 'biology/statistics.html', {
        'progress_records': progress_records,
        'total_lessons': total_lessons,
        'overall_accuracy': overall_accuracy,
        'course_completion': course_completion
    })
