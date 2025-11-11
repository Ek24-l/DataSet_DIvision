from django.db import models

class ARFFFile(models.Model):
    file = models.FileField(upload_to='uploads/')
