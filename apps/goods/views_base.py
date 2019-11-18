from django.views.generic.base import View
from django.http import HttpResponse, JsonResponse
from goods.models import Goods
from django.forms.models import model_to_dict
from django.core import serializers
import json


class GoodsListView(View):
    def get(self, request):
        json_list = []
        goods = Goods.objects.all()[:10]
        for good in goods:
            json_dict = model_to_dict(good)
            json_list.append(json_dict)
        json_data = serializers.serialize('json', goods)

        return JsonResponse(json.loads(json_data), safe=False)
