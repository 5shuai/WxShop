from random import choice

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin
from rest_framework import viewsets, status
from rest_framework.response import Response

from MxShop.settings import API_KEY
from .models import VerifyCode
from utils.yuanpian import YunPian
from .serializers import SmsSerializer, UserRegSerializer

User = get_user_model()


# Create your views here.

class CustomBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            user = User.objects.get(Q(username=username) | Q(mobile=username))
            if user.check_password(password):
                return user
        except Exception as e:
            return None


class SmsCodeViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """发送短信验证码"""
    serializer_class = SmsSerializer

    def generate_code(self):
        """生产四位数字的验证码"""
        seeds = "1234567890"
        random_code = []
        for i in range(4):
            random_code.append(choice(seeds))
        return "".join(random_code)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        mobile = serializer.validated_data["mobile"]
        yun_pian = YunPian(API_KEY)
        code = self.generate_code()
        # sms_status = yun_pian.send_sms(code, mobile)
        sms_status = {"code": 0}
        if sms_status["code"] == 0:
            code_record = VerifyCode(code=code, mobile=mobile)
            code_record.save()
            return Response({
                "mobile": mobile
            }, status=status.HTTP_201_CREATED)
        else:
            return Response({
                "mobile": sms_status["msg"]
            }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(CreateModelMixin, viewsets.GenericViewSet):
    """
    用户
    """
    serializer_class = UserRegSerializer
