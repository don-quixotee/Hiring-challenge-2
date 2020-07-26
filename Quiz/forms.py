from django import forms 
from .models import Subject, Student, User, Question, Answer, Quiz, StudentAnswer
from django.db import transaction
from django.forms.utils import ValidationError




class StudentTopicsForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ('topics',)
        widgets = {
            'topics':forms.CheckboxSelectMultiple
        }


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ('text', )

class BaseAnswerInlineFromSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_one_correct_anser = False
        for form in self.forms:
            if not form.cleaned_data.get('DELETE', False):
                if form.cleaned_data.get('is_correct', False):
                    has_one_correct_anser = True
                    break
        if not has_one_correct_anser:
            raise ValidationError('Mark at least one answer as correct', code = 'no_correct_answer')


class TakeQuizFrom(forms.ModelForm):
    answer = forms.ModelChoiceField(
        queryset=Answer.objects.none(),
        widget = forms.RadioSelect(),
        required = True, empty_label=None
    )

    class Meta:
        model = StudentAnswer
        fields = ['answer']

    def __init__(self, *args, **kwargs):
        question = kwargs.pop('question')
        super().__init__(*args, **kwargs)
        self.fields['answer'].queryset = question.answers.order_by('text')
        

