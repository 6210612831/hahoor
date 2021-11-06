from django import forms
from markdownx.fields import MarkdownxFormField
from thread.models import Thread


class MarkdownForm(forms.Form):
    Content = MarkdownxFormField()


class ThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ['header', 'content']
