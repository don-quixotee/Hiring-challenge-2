from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .forms import StudentSignupForm, TeacherSignUpForm
from .models import User
from django.contrib.auth import login
from Quiz.models import Student 




# Create your views here.
class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class StudentSignUpView(CreateView):
    model = User 
    form_class = StudentSignupForm
    template_name='registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user =form.save()
        login(self.request, user)
        return redirect('student:quiz_list')


class TeacherSignUpView(CreateView):
    model = User 
    form_class=TeacherSignUpForm
    template_name ='registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type']='teacher'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('teachers:quiz_change_list')
