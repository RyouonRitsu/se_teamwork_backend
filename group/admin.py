from django.contrib import admin

from group import models
admin.site.register(models.Group)
admin.site.register(models.Group_Members)
admin.site.register(models.Post)
# Register your models here.
