from django.contrib import admin

from topic import models
admin.site.register(models.Topic)
admin.site.register(models.Topic_Members)
# Register your models here.
