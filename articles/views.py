from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
import constants
from articles.models import Article, Tag
from articles.serializers import ArticleSerializer, TagSerializer, TagSerializerWithoutSlug


class ArticleListCreateAPIView(generics.ListCreateAPIView):
    """
    Class is used for create tags or get the list of tags.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['title', 'content']
    ordering_fields = ['title', 'created_at']


class ArticleDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Class is used for Article retrieve ,update & delete.
    """
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


class TagListCreateAPIView(generics.ListCreateAPIView):
    """
    Class is used for create tags or get the list of tags.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class TagDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """
    Class is used for tag retrieve ,update & delete.
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

    def get_serializer_class(self):
        """
        Function is used to override serializers.
        :return: serializer class
        """
        serializer_class = self.serializer_class
        tag = self.get_object()
        tag_article = tag.article_set.all()
        if self.request.method == 'PUT' and tag_article:
            serializer_class = TagSerializerWithoutSlug
        return serializer_class

    def delete(self, request, *args, **kwargs):
        """
        Function is used to delete tags or value in table and return status.
        :param request: request header with info.
        :return: success or fail response
        """
        tag = self.get_object()
        if not tag.article_set.all():
            tag.delete()
            super().delete(request, *args, **kwargs)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({"message": constants.FAIL_MESSAGES['DELETE_TAG_FAIL']},
                        status=status.HTTP_400_BAD_REQUEST)


class ArticlesByTagAPIView(generics.ListAPIView):
    """
    Class is used for filtering Articles by tag.
    """
    serializer_class = ArticleSerializer

    def get_queryset(self):
        """
        Function is used to add tags to the Article or value in table and return status.
        :return: Article queryset
        """
        tags_id = self.kwargs['tag_id']
        return Article.objects.filter(tags__id=tags_id)


class AddTagToArticle(APIView):
    """
    Class is used for Adding  tags to the Article.
    """

    def post(self, request, article_id):
        """
        Function is used to add tags to the Article or value in table and return status.
        :param request: request header with info for updating new object.
        :return: tag list
        """
        tag_list = request.data.get(constants.REQUEST_PARAMS['PARAM_TAG_ID_LIST'])
        if not tag_list:
            return Response({"message": constants.REQUEST_PARAMS['MISSING_PARAM'].format(
                constants.REQUEST_PARAMS['PARAM_TAG_ID_LIST'])}, status=status.HTTP_400_BAD_REQUEST)
        try:
            article = Article.objects.get(id=article_id)
            for tag_id in tag_list:
                tag = Tag.objects.get(id=int(tag_id))
                article.tags.add(tag)
            return Response({"message": constants.SUCCESS_MESSAGES['ADD_ARTICLE_TAG_SUCCESS']},
                            status=status.HTTP_200_OK)
        except:
            return Response({"message": constants.FAIL_MESSAGES['ADD_ARTICLE_TAG_FAIL']},
                            status=status.HTTP_400_BAD_REQUEST)


class RemoveTagFromArticle(APIView):
    """
        Class is used for remove tag from the article.
    """

    def post(self, request, article_id):
        """
        Function is used to remove tag from the article and return status.
        :param request: request header with info for updating new object.
        :return: tag list
        """
        tag_id = request.data.get(constants.REQUEST_PARAMS['PARAM_TAG_ID'])
        if not tag_id:
            return Response({"message": constants.REQUEST_PARAMS['MISSING_PARAM'].format(
                constants.REQUEST_PARAMS['PARAM_TAG_ID'])}, status=status.HTTP_400_BAD_REQUEST)
        try:
            article = Article.objects.get(id=article_id)
            tag = Tag.objects.get(id=int(tag_id))
            article.tags.remove(tag)
            return Response({"message": constants.SUCCESS_MESSAGES['REMOVE_ARTICLE_TAG_SUCCESS']},
                            status=status.HTTP_200_OK)
        except:
            return Response({"message": constants.FAIL_MESSAGES['REMOVE_ARTICLE_TAG_FAIL']},
                            status=status.HTTP_400_BAD_REQUEST)
