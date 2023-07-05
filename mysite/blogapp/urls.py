from django.urls import path

from .views import ArticleView

app_name = "blogapp"

urlpatterns = [
    path("articles/", ArticleView.as_view(), name="articles")
]