import factory

from articles.models import Article, Tag


class ArticleFactory(factory.django.DjangoModelFactory):
    title = factory.Sequence(lambda n: f"Article {n}")
    slug = factory.Sequence(lambda n: f"article-{n}")

    class Meta:
        model = Article


class TagFactory(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: f"Tag {n}")
    slug = factory.Sequence(lambda n: f"Tag-{n}")

    class Meta:
        model = Tag
