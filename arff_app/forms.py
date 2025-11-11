from django.forms import ModelForm
from .models import ARFFFile

class ARFFUploadForm(ModelForm):
    class Meta:
        model = ARFFFile
        fields = ['file']
