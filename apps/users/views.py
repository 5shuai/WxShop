from random import choice

from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin
from rest_framework import viewsets, status, permissions
from rest_framework.response import Response
from rest_framework_jwt.serializers import jwt_encode_handler, jwt_payload_handler
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework.authentication import SessionAuthentication
from MxShop.settings import API_KEY
from .models import VerifyCode
from utils.yuanpian import YunPian
from .serializers import SmsSerializer, UserRegSerializer, UserDetailSerializer

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


class UserViewSet(CreateModelMixin, RetrieveModelMixin, viewsets.GenericViewSet, UpdateModelMixin):
    """
    用户
    """
    serializer_class = UserRegSerializer
    queryset = User.objects.all()
    authentication_classes = (JSONWebTokenAuthentication, SessionAuthentication)

    def get_permissions(self):
        if self.action == 'retrieve':
            return [permissions.IsAuthenticated()]
        elif self.action == 'create':
            return []
        return []

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return UserDetailSerializer
        elif self.action == 'create':
            return UserRegSerializer
        return UserDetailSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        re_dict = serializer.data
        payload = jwt_payload_handler(user)
        re_dict["token"] = jwt_encode_handler(payload)
        re_dict["name"] = user.name if user.name else user.username

        headers = self.get_success_headers(serializer.data)
        return Response(re_dict, status=status.HTTP_200_OK, headers=headers)

    def get_object(self):
        return self.request.user

    def perform_create(self, serializer):
        return serializer.save()
