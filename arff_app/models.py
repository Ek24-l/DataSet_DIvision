# arff_app/models.py
from django.db import models

class ARFFFile(models.Model):
    file = models.FileField(upload_to='arffs/')
    uploaded_at = models.DateTimeField(auto_now_add=True)  # fecha de subida automática

    def __str__(self):
        return self.file.name
