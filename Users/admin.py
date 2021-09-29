from django.contrib import admin
from .models import Profile, Question, Submissions

# code to register models

admin.site.register(Profile)
admin.site.register(Question)
admin.site.register(Submissions)
