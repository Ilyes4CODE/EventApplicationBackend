from django.contrib import admin
from .models import Ticket,Profile,Events
# Register your models here.
admin.site.register(Ticket)
admin.site.register(Profile)
admin.site.register(Events)
