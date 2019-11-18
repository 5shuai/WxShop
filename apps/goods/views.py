# Create your views here.

from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets
from .models import Goods
from .serializers import GoodsSerializer


class GoodsPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    page_query_param = "page"
    max_page_size = 100


class GoodsListView(generics.ListAPIView):
    """
    List all goods.
    """
    queryset = Goods.objects.all()
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
