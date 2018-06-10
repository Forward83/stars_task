from django import forms
from django.forms.widgets import TextInput
from .models import Book, HttpRequest


class DateInput(forms.DateInput):
    input_type = 'date'


class BookForm(forms.ModelForm):
    new_authors = forms.CharField(max_length=40, required=False)

    class Meta:
        model = Book
        fields = ['title', 'ISBN', 'publish_date', 'price', 'author', 'new_authors', 'image']
        # labels = {''}
        help_texts = {'new_authors': 'If there are multiple authors, separate them by comma'}
        # widgets = {'publish_date': forms.DateInput(attrs={'class': 'datepicker'}),}
        widgets = {'title': TextInput(attrs={'class': 'field-long'}),
                    'publish_date': DateInput(),
                   }

class RequestForm(forms.ModelForm):

    class Meta:
        model = HttpRequest
        fields = '__all__'
