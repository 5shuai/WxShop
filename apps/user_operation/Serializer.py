from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.models import Goods
from .models import UserFav, UserLeavingMessage
from goods.serializers import GoodsSerializer


class UserFavDetailSerializer(serializers.ModelSerializer):
    goods = GoodsSerializer()

    class Meta:
        model = UserFav
        fields = ("goods", "id")


class UserFavSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserFav
        validators = [
            UniqueTogetherValidator(
                queryset=UserFav.objects.all(),
                fields=('user', 'goods'),
                message="你已经收藏过此商品"
            )
        ]
        fields = ("user", "goods", "id")


class LeavingMessageSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserLeavingMessage
        fields = ("user", "message_type", "subject", "message", "file", "id", "add_time")
