from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic import ListView
from .models import Article

class ArticleView(ListView):
    template_name = "blogapp/article_list.html"
    context_object_name = "articles"
    model = Article
    queryset = Article.objects.defer("content").select_related("author","category").prefetch_related("tags")
