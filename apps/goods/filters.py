import django_filters
from django.db.models import Q
from .models import Goods


class GoodsFilter(django_filters.rest_framework.FilterSet):
    pricemin = django_filters.NumberFilter(field_name='shop_price', lookup_expr='gte', help_text="最低价格")
    pricemax = django_filters.NumberFilter(field_name='shop_price', lookup_expr='lte', help_text="最高价格")
    top_category = django_filters.NumberFilter(method='top_category_filter', help_text="categoryId")
    is_hot = django_filters.NumberFilter(field_name='is_hot',help_text="1为热销，0为非热销")
    is_new = django_filters.NumberFilter(field_name='is_new',help_text="1为新品，0为非新品")

    def top_category_filter(self, queryset, name, value):
        return queryset.filter(Q(category_id=value) | Q(category__parent_category_id=value) | Q(
            category__parent_category__parent_category_id=value))

    class Meta:
        model = Goods
        fields = ['pricemin', 'pricemax', 'is_hot', 'is_new']
