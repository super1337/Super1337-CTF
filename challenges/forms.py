from django import forms


class FlagForm(forms.Form):
    flag = forms.CharField(label='flag', max_length=256)
