"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from articles.views import ArticleDetailAPIView, ArticleListCreateAPIView, TagListCreateAPIView, TagDetailAPIView, \
    AddTagToArticle, \
    RemoveTagFromArticle, ArticlesByTagAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/articles/", ArticleListCreateAPIView.as_view(), name="article_list"),
    path("api/articles/<int:pk>/", ArticleDetailAPIView.as_view(), name="article_detail"),
    path("api/tags/", TagListCreateAPIView.as_view(), name="tag_list"),
    path("api/tags/<int:pk>/", TagDetailAPIView.as_view(), name="tag_detail"),
    path("api/article-by-tag/<int:tag_id>/", ArticlesByTagAPIView.as_view(), name="article_list_by_tag"),
    path("api/add-article-tag/<int:article_id>/", AddTagToArticle.as_view(), name="add-article-tag"),
    path("api/remove-article-tag/<int:article_id>/", RemoveTagFromArticle.as_view(), name="remove-article-tag'")
]
