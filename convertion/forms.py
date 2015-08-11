from django import forms

class ConvertForm(forms.Form):
    number = forms.IntegerField(label='Enter a number')