from django.urls import path , include
from .views import home, QuizListView, QuizCreateView, QuizDeleteView, QuizResultView, QuizUpdateView,CourseCreateView, CourseListView, question_add, question_change, QuestionDeleteView






urlpatterns = [
    path('', home , name='home'),
    path('teachers/', QuizListView.as_view(), name='quiz_change_list'),
    path('teachers/quiz/add/', QuizCreateView.as_view(), name = 'quiz_add'),
    path('teachers/course/add',CourseCreateView.as_view(), name='course_add'),
    path('teachers/course/list', CourseListView.as_view(), name='course_change_list'),
    path('teachers/quiz/<int:pk>/', QuizUpdateView.as_view(), name='quiz_change'),
    path('teachers/quiz/<int:pk>/delete/', QuizDeleteView.as_view(), name='quiz_delete'),
    path('teachers/quiz/<int:pk>/results/', QuizResultView.as_view(), name ='quiz_result'),
    path('teachers/quiz/<int:pk>/question/add/', question_add, name='question_add'),
    path('teachers/quiz/<int:quiz_pk>/question/<int:question_pk>/', question_change, name='question_change'),
    path('teachers/quiz/<int:quiz_pk>/question/<int:question_pk>/delete/', QuestionDeleteView.as_view(), name='question_delete'),
    



]