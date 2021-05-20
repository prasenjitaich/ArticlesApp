from rest_framework import serializers

from articles.models import Article, Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class ArticleSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Article
        fields = "__all__"


class TagSerializerWithoutSlug(serializers.ModelSerializer):
    class Meta:
        model = Tag
        exclude = ('slug',)
