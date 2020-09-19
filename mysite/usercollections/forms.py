from django import forms
from usercollections.models import Collection
from books.models import Books

class CreateACollectionForm(forms.ModelForm):
    '''
    Custom Form to create a named collection
    '''
    collectionName = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Collection
        fields = ('collectionName','description')

    def clean(self):
        collectionName = self.cleaned_data['collectionName']
        if collectionName == '':
            raise forms.ValidationError('Collection Name cannot be empty')


class AddBookISBNForm(forms.ModelForm):
    '''
    This form allows users to add books to a collection using ISBN
    '''
    ISBN = forms.CharField(max_length=50)

    class Meta:
        model = Books
        fields = ('ISBN',)

    def clean(self):
        isbn = self.cleaned_data['ISBN']
        try:
            book = Books.objects.get(ISBN=isbn)
        except Books.DoesNotExist:
            raise forms.ValidationError('Book "%s" does not exist.' % isbn)
