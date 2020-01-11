from django.contrib import admin
from .models import EmailObject, Attachment, Recipient


admin.site.register(EmailObject)
admin.site.register(Attachment)
admin.site.register(Recipient)
