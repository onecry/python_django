from django.contrib import admin

from .models import Article, Author, Category, Tag


admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Tag)
