from django import forms
from goals.models import Goal
from books.models import Books

class AddGoalForm(forms.ModelForm):
    '''
    allows user to add goal 
    '''
    class Meta:
        model = Goal
        fields = ['UID','numBooks']

    def clean(self):
        self.cleaned_data['numBooks']
        
