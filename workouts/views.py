from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum
from .models import Workout, WorkoutExercise, Exercise
from .forms import WorkoutForm, WorkoutExerciseForm, UserRegisterForm, ExerciseForm

# Create your views here.

@login_required
def workout_list(request):
    workouts = Workout.objects.filter(user=request.user).prefetch_related('workout_exercises')
    return render(request, 'workout_list.html', {'workouts': workouts})


@login_required
def add_workout(request):
    if request.method == 'POST':
        form = WorkoutForm(request.POST)
        if form.is_valid():
            workout = form.save(commit=False)
            workout.user = request.user
            workout.save()
            return redirect('workout_list')
    else:
        form = WorkoutForm()
    return render(request, 'add_workout.html', {'form': form})

@login_required
def workout_detail(request, pk):
    workout = Workout.objects.get(id=pk, user=request.user)
    exercises = WorkoutExercise.objects.filter(workout=workout)
    return render(request, 'workout_detail.html', {'workout': workout, 'exercises': exercises})

@login_required
def add_exercise(request, pk):
    workout = Workout.objects.get(id=pk, user=request.user)
    if request.method == 'POST':
        form = WorkoutExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.workout = workout
            exercise.save()
            return redirect('workout_detail', pk=workout.id)
    else:
        form = WorkoutExerciseForm()
    return render(request, 'add_exercise.html', {'form': form, 'workout': workout})

@login_required
def exercise_detail(request, workout_id, exercise_id):
    try:
        workout = Workout.objects.get(id=workout_id, user=request.user)
        exercise = WorkoutExercise.objects.get(id=exercise_id, workout=workout)
    except (Workout.DoesNotExist, WorkoutExercise.DoesNotExist):
        messages.error(request, "Тренировка или упражнение не найдены.")
        return redirect('workout_list')
    
    return render(request, 'exercise_detail.html', {'workout': workout, 'exercise': exercise})



@login_required
def progress_report(request):
    workouts = Workout.objects.filter(user=request.user)

    total_workouts = workouts.count()
    total_sets = WorkoutExercise.objects.filter(workout__in=workouts).aggregate(Sum('sets'))['sets__sum'] or 0
    total_reps = WorkoutExercise.objects.filter(workout__in=workouts).aggregate(Sum('reps'))['reps__sum'] or 0
    total_weight = WorkoutExercise.objects.filter(workout__in=workouts).aggregate(Sum('weight'))['weight__sum'] or 0

    last_30_days = timezone.now() - timezone.timedelta(days=30)
    recent_workouts = workouts.filter(date__gte=last_30_days)
    recent_sets = WorkoutExercise.objects.filter(workout__in=recent_workouts).aggregate(Sum('sets'))['sets__sum'] or 0
    recent_reps = WorkoutExercise.objects.filter(workout__in=recent_workouts).aggregate(Sum('reps'))['reps__sum'] or 0
    recent_weight = WorkoutExercise.objects.filter(workout__in=recent_workouts).aggregate(Sum('weight'))['weight__sum'] or 0

    context = {
        'total_workouts': total_workouts,
        'total_sets': total_sets,
        'total_reps': total_reps,
        'total_weight': total_weight,
        'recent_sets': recent_sets,
        'recent_reps': recent_reps,
        'recent_weight': recent_weight,
    }

    return render(request, 'progress_report.html', context)



@login_required
def create_exercise(request):
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save()
            messages.success(request, f'Упражнение {exercise.name} успешно создан!')
            return redirect('workout_list')
    else:
        form = ExerciseForm()
    return render(request, 'create_exercise.html', {'form': form})





def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт для {username} успешно создан! Теперь вы можете войти.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})
