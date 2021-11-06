from django import forms
from markdownx.fields import MarkdownxFormField


class MarkdownForm(forms.Form):
    Content = MarkdownxFormField()
