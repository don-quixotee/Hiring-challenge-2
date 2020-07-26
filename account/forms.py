from django import forms 
from django.contrib.auth.forms import UserCreationForm
from .models import User
from Quiz.models import Subject, Student




class StudentSignupForm(UserCreationForm):
    topics = forms.ModelMultipleChoiceField(
        queryset = Subject.objects.all(), 
        widget = forms.CheckboxSelectMultiple,
        required=True
    )
    class Meta(UserCreationForm.Meta):
        model = User


    def save(self):
        user= super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        student.topics.add(*self.cleaned_data.get('interests'))
        return user 





class TeacherSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User 

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_teacher = True
        if commit:
            user.save()
        return user 


