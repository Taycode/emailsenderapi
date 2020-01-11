from django.contrib import admin
from .models import EmailObject, Attachment


admin.site.register(EmailObject)
admin.site.register(Attachment)
