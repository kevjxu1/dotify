from django import forms

class GenerateForm(forms.Form):
    outH = forms.IntegerField(initial=20, min_value=1)
    outW = forms.IntegerField(initial=40, min_value=1)
    thresh = forms.IntegerField(initial=135)
    imageFile = forms.FileField()
    reverse = forms.BooleanField(required=False)

