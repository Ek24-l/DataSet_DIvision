# arff_app/forms.py
from django import forms
from .models import ARFFFile

class ARFFUploadForm(forms.ModelForm):
    class Meta:
        model = ARFFFile
        fields = ['file']

