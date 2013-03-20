from django import forms
from django.forms import ModelForm, Textarea
from .models import Passage


class PassageForm(ModelForm):
    location = forms.CharField(required=False,
                widget=forms.TextInput(attrs={'placeholder': 'location'}))
    text = forms.CharField(
                widget=forms.Textarea(attrs={'placeholder': 'highlighted text'}))

    class Meta:
        model = Passage
        fields = ('book', 'location', 'text')
        #widgets = {
        #    'name': Textarea(attrs={'cols': 80, 'rows': 20}),
        #}
