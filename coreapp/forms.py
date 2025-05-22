from django import forms
from .models import ReviewsModel

RATING_CHOICES = [(i, f'{i} Star') for i in range(1, 6)]
class ReviewsForm(forms.ModelForm):
    rating = forms.ChoiceField(
    choices=RATING_CHOICES,
    widget=forms.RadioSelect(attrs={'class': 'star-rating'})
    )
    
    class Meta:
        model = ReviewsModel
        fields = ['rating', 'review', 'review_image']