from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from goods.models import Goods
from .models import UserFav, UserLeavingMessage, UserAddress
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


class AddressSerializer(serializers.ModelSerializer):
    add_time = serializers.DateTimeField(read_only=True, format="%Y-%m-%d %H:%M:%S")
    province = serializers.CharField(required=True,help_text="省", error_messages={
        "required": "该字段不能为空"
    })
    city = serializers.CharField(required=True, help_text="市",error_messages={
        "required": "该字段不能为空"
    })
    district = serializers.CharField(required=True, help_text="区",error_messages={
        "required": "该字段不能为空"
    })
    address = serializers.CharField(required=True, help_text="收货地址", error_messages={
        "required": "该字段不能为空"
    })
    signer_name = serializers.CharField(required=True,help_text="收货人姓名", error_messages={
        "required": "该字段不能为空"
    })
    signer_mobile = serializers.CharField(required=True, help_text="手机号",error_messages={
        "required": "该字段不能为空"
    })

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = UserAddress
        fields = "__all__"
