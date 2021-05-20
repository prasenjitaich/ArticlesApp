from django.db import models


class ParentTag(models.Model):
    parent_name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.parent_name


class Tag(models.Model):
    name = models.CharField(max_length=200, unique=True)
    slug = models.CharField(max_length=32, unique=True)
    parent_tag = models.ForeignKey(ParentTag, on_delete=models.CASCADE, blank=True, null=True, related_name="tags")

    def __str__(self):
        return self.name


class Article(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=32)
    slug = models.CharField(max_length=32, unique=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag, blank=True)

    class Meta:
        ordering = ["id"]

    def __str__(self):
        return self.title
