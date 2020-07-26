from django.urls import path , include
from .views import StudentSignUpView, SignUpView, TeacherSignUpView




urlpatterns = [
    path('',include('django.contrib.auth.urls')),
    path('signup/', SignUpView.as_view(), name = 'signup'),
    path('signup/student/',StudentSignUpView.as_view(), name='student_signup'),
    path('signup/teacher/', TeacherSignUpView.as_view(), name='teacher_signup'),
]