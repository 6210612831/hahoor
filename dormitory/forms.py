from django import forms
from dormitory.models import Dormitory
from markdownx.fields import MarkdownxFormField


class MarkdownForm(forms.Form):
    Content = MarkdownxFormField()


class DormitoryForm(forms.ModelForm):
    class Meta:
        model = Dormitory
        fields = ['title', 'desc', 'content']
