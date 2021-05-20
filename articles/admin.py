from django.contrib import admin

from articles.models import Article, Tag, ParentTag

admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(ParentTag)
