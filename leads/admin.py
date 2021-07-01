from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register([User, Lead, Agent, UserProfile, Category])
admin.site.site_header = 'django crm'
