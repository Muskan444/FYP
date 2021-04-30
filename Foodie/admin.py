from django.contrib import admin
from .models import profile, Blogs, Review

# Register your models here.

admin.site.register(profile)
admin.site.register(Blogs)
admin.site.register(Review)