from django import forms

class SearchForm(forms.Form):
    q = forms.CharField(label='Search', max_length=100, widget=forms.TextInput(attrs={
        'class': 'form-control me-2',
        'placeholder': 'Search news, country, topic...',
        'type': 'search',
        'aria-label': 'Search'
    }))
