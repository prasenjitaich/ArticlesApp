from django.test import TestCase

from articles.tests.factories import ArticleFactory


class ArticleTest(TestCase):
    def test_str(self):
        article = ArticleFactory(title="Test Title")
        self.assertEqual(str(article), "Test Title")
