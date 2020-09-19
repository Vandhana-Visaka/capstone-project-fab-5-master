from django import forms
from review.models import Review

class AddReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(1)]
    )
    review = forms.CharField(widget=forms.Textarea, required=False)

    class Meta:
        model = Review
        fields = ('rating','review')