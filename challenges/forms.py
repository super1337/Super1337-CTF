from django import forms


class FlagForm(forms.Form):
    flag = forms.CharField(label='flag', max_length=256)


class SortOrderForm(forms.Form):
    choices = [
        (1, 'name'),
        (2, 'score'),
        (3, 'created'),
        (4, 'modified')
    ]
    sortorder = forms.ChoiceField(label='sort order', choices=choices,
                                  widget=forms.Select(attrs={"onChange": 'refresh()'}))
