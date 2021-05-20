from rest_framework import status
from rest_framework.test import APITestCase

from django.urls import reverse
from django.utils.http import urlencode

from articles.models import Article, Tag
from articles.tests.factories import ArticleFactory, TagFactory


class ArticleListCreateAPIViewTest(APITestCase):
    def test_article_list(self):
        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(reverse("article_list"))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            [article["id"] for article in response.data], [article1.id, article2.id]
        )

    def test_article_create(self):
        self.assertEqual(Article.objects.count(), 0)
        data = {
            "title": "Test Article",
            "slug": "test-article",
            "content": "Lorem ipsum",
        }
        response = self.client.post(reverse("article_list"), data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(id=response.data["id"])  # newly-created
        self.assertEqual(article.slug, "test-article")

    def test_article_filter(self):
        def build_url(*args, **kwargs):
            params = kwargs.pop('params', {})
            url = reverse(*args, **kwargs)
            if params:
                url += '?' + urlencode(params)
            return url

        article1, article2 = ArticleFactory.create_batch(2)
        response = self.client.get(build_url('article_list', params={'title': article1.title}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        article = Article.objects.filter(title=response.data[0]["title"]).first()
        self.assertEqual(article.title, "Article 3")

    def test_article_order(self):
        def build_url(*args, **kwargs):
            params = kwargs.pop('params', {})
            url = reverse(*args, **kwargs)
            if params:
                url += '?' + urlencode(params)
            return url

        article1, article2, article3 = ArticleFactory.create_batch(3)
        response1 = self.client.get(build_url('article_list', params={'ordering': '-title'}))
        self.assertEqual(response1.status_code, status.HTTP_200_OK)
        self.assertEqual(article3.title, response1.data[0]["title"])
        self.assertEqual(article2.title, response1.data[1]["title"])
        self.assertEqual(article1.title, response1.data[2]["title"])
        response2 = self.client.get(build_url('article_list', params={'ordering': '-created_at'}))
        self.assertEqual(response2.status_code, status.HTTP_200_OK)
        self.assertEqual(article3.id, response1.data[0]["id"])
        self.assertEqual(article2.id, response1.data[1]["id"])
        self.assertEqual(article1.id, response1.data[2]["id"])


class ArticleDetailAPIViewTest(APITestCase):
    def test_article_update(self):
        article = ArticleFactory(slug="my-slug")
        data = {"slug": "updated-slug"}
        url = reverse("article_detail", args=(article.id,))
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_article = Article.objects.get(id=article.id)
        self.assertEqual(updated_article.slug, "updated-slug")

    def test_article_delete(self):
        article = ArticleFactory()
        url = reverse("article_detail", args=(article.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Article.objects.count(), 0)


class TagDetailAPIViewTest(APITestCase):
    def test_tag_update(self):
        tag = TagFactory(name="my-tag")
        data = {"slug": "updated-slug"}
        url = reverse("tag_detail", args=(tag.id,))
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_tag = Tag.objects.get(id=tag.id)
        self.assertEqual(updated_tag.slug, "updated-slug")
        article1 = ArticleFactory()
        article1.tags.add(tag)
        data = {"slug": "new-updated-slug"}
        response = self.client.patch(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(updated_tag.slug, "updated-slug")
        self.assertNotEqual(updated_tag.slug, "new-updated-slug")

    def test_tag_delete(self):
        tag = TagFactory()
        url = reverse("tag_detail", args=(tag.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tag.objects.count(), 0)
        article1 = ArticleFactory()
        tag1 = TagFactory()
        article1.tags.add(tag1)
        url = reverse("tag_detail", args=(tag1.id,))
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Tag.objects.count(), 1)
