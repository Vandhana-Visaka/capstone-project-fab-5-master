from django import forms
from books.models import Books

class BookForm(forms.ModelForm):
    '''
    Custome Form to help users insert books into website
    widgets to make form look good using bootstrap settings
    '''
    class Meta:
        model = Books
        fields = ('ISBN','title','authors','genres','summary','language','country','num_page','cover','publisher','publication_date')
        widgets = {
            'ISBN' : forms.TextInput(attrs={'class' : 'form-control'}),
            'title' : forms.TextInput(attrs={'class': 'form-control'}),
            'authors' : forms.TextInput(attrs={'class': 'form-control'}),
            'genres' : forms.TextInput(attrs={'class': 'form-control'}),
            'summary' : forms.TextInput(attrs={'class': 'form-control'}),
            'language' : forms.TextInput(attrs={'class': 'form-control'}),
            'country' : forms.TextInput(attrs={'class': 'form-control'}),
            'num_page' : forms.TextInput(attrs={'class': 'form-control'}),
            'publisher' : forms.TextInput(attrs={'class':'form-control'}),
            'publication_date': forms.TextInput(attrs={'class': 'form-control'})
        }
