from django.contrib import admin
from watchlist_app import models
# Register your models here.

admin.site.register(models.streamplatform)
admin.site.register(models.watchlist)
admin.site.register(models.Review)