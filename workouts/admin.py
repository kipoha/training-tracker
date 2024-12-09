from django.contrib import admin
from .models import Exercise, Workout, WorkoutExercise

# Register your models here.

admin.site.register(Exercise)
admin.site.register(Workout)
admin.site.register(WorkoutExercise)
