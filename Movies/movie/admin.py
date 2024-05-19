from django.contrib import admin

# Register your models here.
from .models import Category, Movie, Comment, Rating

admin.site.register(Category)
admin.site.register(Movie)
#admin.site.register(User)
admin.site.register(Comment)
admin.site.register(Rating)