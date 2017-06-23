'''
from .models import Document

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ('description', 'document', )
'''

from django import forms


class FlagForm(forms.Form):
    flag = forms.CharField(label='flag', max_length=256)
