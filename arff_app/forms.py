# arff_app/forms.py
from django import forms

class ARFFUploadForm(forms.Form):
    file = forms.FileField(
        label="Archivo ARFF",
        required=True,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )

