from django import forms

class ARFFUploadForm(forms.Form):
    file = forms.FileField()
