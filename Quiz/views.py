from django.shortcuts import render, redirect, get_object_or_404
from django.forms import inlineformset_factory
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Avg, Count
from django.http import HttpResponse
from .models import Answer, Question, Quiz, Student, Subject
from account.models import User 
from django.contrib import messages
from .forms import BaseAnswerInlineFromSet, QuestionForm
from django.db import transaction



# Create your views here.

def home(request):
    if request.user.is_authenticated:
        if request.user.is_teacher:
            return redirect('quiz_change_list')
        else:
            return redirect('quiz_list')
    return render(request, 'Quiz/home.html')
    

class QuizListView(ListView):
    model = Quiz
    ordering=('name', )
    context_object_name = 'quizzes'
    template_name = 'Quiz/teachers/quiz_change_list.html'

    def get_queryset(self):
        queryset = self.request.user.quizzes.select_related('subject').annotate(questions_count=Count('questions', distinct=True)).annotate(taken_count=Count('taken_quizzes',distinct=True))
        return queryset


class QuizCreateView(CreateView):
    model = Quiz
    fields = ['name', 'subject','duration' ]
    template_name = 'Quiz/teachers/quiz_add_form.html'

    def form_valid(self,form):
        quiz = form.save(commit=False)
        quiz.owner = self.request.user 
        quiz.save()
        messages.success(self.request, 'the quiz has been create! add some questions to it')
        return redirect('quiz_change', quiz.pk)


class QuizUpdateView(UpdateView):
    model = Quiz
    fields = ['name', 'subject', 'duration']
    context_onject_name = 'quiz'
    template_name = 'Quiz/teachers/quiz_change_form.html'

    def get_context_data(self, **kwargs):
        kwargs['questions']=self.get_object().questions.annotate(answers_count=Count('answers'))
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()

    def get_success_url(self):
        return reverse('quiz_change', kwargs=={'pk':self.object.pk})


class QuizDeleteView(DeleteView):
    model = Quiz
    context_object_name = 'Quiz/teachers/quiz_delete.html'
    success_url = reverse_lazy('quiz_change_list')

    def  delete(self, request, *args, **kwargs):
        quiz = self.get_object()
        messages.success(request, 'The Quiz %s was deleted with Success !'% quiz.name)

        return super().delete(request, *args, **kwargs)
    def get_queryset(self):
        return self.request.quizzes.all()



class QuizResultView(DetailView):
    model = Quiz
    context_object_name = 'quiz'
    template = 'Quiz/teachers/quiz_result.html'

    def get_context_data(self, **kwargs):
        quiz = self.get_object()
        taken_quizzes = quiz.taken_quizzes.select_releted('student__user').order_by('-date')
        total_taken_Quizzes = taken_quizzes.count()
        quiz_score = quiz.taken_quizzes.aggregate(average_score=Avg('score'))
        extra_context = {
            'taken_quizzes':taken_quizzes,
            'total_taken_quizzes': total_taken_Quizzes,
            'quiz_score':quiz_score

        }
        kwargs.update(extra_context)
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        return self.request.user.quizzes.all()



def question_add(request, pk):
    quiz = get_object_or_404(Quiz, pk=pk, owner=request.user)
    if request.method =="POST":
        form = QuestionFrom(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.quiz = quiz 
            question.save()
            messages.success(request, 'please add answer option to the question')
            return redirect('question_change', quiz.pk, question.pk)

    else:
        form = QuestionFrom()
    return render(request, 'Quiz/teachers/question_add_form.html', {'quiz':quiz, 'form':form})


def question_change(request, quiz_pk, question_pk):
    quiz = get_object_or_404(Quiz, pk=quiz_pk, owner=request.user)
    question = get_object_or_404(Question, pk=question_pk, quiz=quiz)

    AnswerFormSet = inlineformset_factory(
        Question, Answer, 
        formset=BaseAnswerInlineFromSet,
        fields = ['text', 'is_correct'],
        min_num = 2,
        validate_min = True,
        max_num = 10,
        validate_max = True
        )
    if request.method == 'POST':
        form = QuestionForm(request.POST, instance=question)
        formset = AnswerFormSet(request.POST, instance=question)
        if form.is_valid() and formset.is_valid():
            with transaction.atomic():
                form.save()
                formset.save()

            messages.success(request, 'Question and answer saved with success')
            return redirect('quiz_change', quiz.pk)
    else:
        form = QuestionForm(instance=question)
        formset = AnswerFormSet(instance=question)
    context = {'quiz':quiz, 'question':question, 'form':form, 'formset':formset}

    return render(request, 'Quiz/teachers/question_change_form.html', context)



class QuestionDeleteView(DeleteView):
    model = Question
    context_onject_name = 'question'
    template_name = 'Quiz/teachers/question_delete.html'
    pk_url_kwarg = 'question_pk'
    def get_context_data(self, **kwargs):
        question = self.get_object()
        kwargs['quiz'] = question.quiz
        return super().get_context_data(**kwargs)

    def delete(self, request, *args, **kwargs):
        question = self.get_object()
        messages.success(request, 'The question %s was deleted with success!' % question.text)
        return super().delete(request, *args, **kwargs)

    def get_queryset(self):
        return Question.objects.filter(quiz__owner=self.request.user)

    def get_success_url(self):
        question = self.get_object()
        return reverse('quiz_change', kwargs={'pk': question.quiz_id})








        
class CourseListView(ListView):
    model = Subject
    ordering = ('name',)
    context_object_name = 'courses'
    template_name = 'Quiz/teachers/course_change_list.html'

    
class CourseCreateView(CreateView):
    model = Subject
    fields = ('name', 'color',)
    template_name = 'Quiz/teachers/course_add_form.html'

    def form_valid(self, form):
        course = form.save(commit=False)
        course.owner = self.request.user
        course.save()
        messages.success(self.request, 'The class was created with success! Go ahead and add a quiz now.')
        return redirect('home')

