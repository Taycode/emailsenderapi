from django.db import models
from django.contrib.auth.models import User


class Attachment(models.Model):
    file = models.FileField(upload_to='files')


class EmailObject(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    subject = models.CharField(max_length=100)
    body = models.TextField(blank=True)
    attachments = models.ManyToManyField(Attachment, blank=True)
