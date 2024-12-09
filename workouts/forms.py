from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Workout, WorkoutExercise, Exercise

# class WorkoutForm(forms.ModelForm):
#     class Meta:
#         model = Workout
#         fields = ['date', 'exercises']

# class WorkoutExerciseForm(forms.ModelForm):
#     class Meta:
#         model = WorkoutExercise
#         fields = ['exercise', 'repetitions', 'sets']

# from django import forms
# from .models import Workout, WorkoutExercise

class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['exercise', 'sets', 'reps', 'weight']


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ['name', 'description']



class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
