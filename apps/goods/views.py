# Create your views here.

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import mixins, viewsets
from .models import Goods, GoodsCategory
from .serializers import GoodsSerializer, CategorySerializer


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GoodsListView(mixins.ListModelMixin, viewsets.GenericViewSet):
    """
    List all goods.
    """
    queryset = Goods.objects.get_queryset().order_by('id')
    serializer_class = GoodsSerializer
    pagination_class = GoodsPagination

    # def get(self, request, format=None):
    #     goods = Goods.objects.all()[:10]
    #     serializer = GoodsSerializer(goods, many=True)
    #     return Response(serializer.data)
    #
    # def post(self, request):
    #     serializer = GoodsSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = GoodsCategory.objects.filter(category_type=1)
    serializer_class = CategorySerializer
