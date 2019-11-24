"""MxShop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import include
from django.urls import path
from django.views.static import serve
from rest_framework.documentation import include_docs_urls
from rest_framework.routers import DefaultRouter
import xadmin
from MxShop.settings import MEDIA_ROOT
from goods.views import GoodsListView, CategoryViewSet
from rest_framework.authtoken import views
from rest_framework_jwt.views import obtain_jwt_token

from user_operation.views import UserFavViewSet, LeavingMessageViewSet
from users.views import SmsCodeViewSet, UserViewSet

router = DefaultRouter()
router.register(r'goods', GoodsListView, base_name="goods")
router.register(r'categories', CategoryViewSet, base_name="categories")
router.register(r'code', SmsCodeViewSet, base_name="code")
router.register(r'users', UserViewSet, base_name="users")
router.register(r'userfavs', UserFavViewSet, base_name="userfavs")
router.register(r'messages', LeavingMessageViewSet, base_name="messages")
goods_list = GoodsListView.as_view({
    'get': 'list'
})

urlpatterns = [
    path('media/<path:path>', serve, {'document_root': MEDIA_ROOT}),
    path('ueditor/', include('DjangoUeditor.urls')),
    path('xadmin/', xadmin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('docs/', include_docs_urls(title="美客生鲜")),
    # drf自带的token认证模式
    path('api-token-auth/', views.obtain_auth_token),
    # jwt的认证模式
    path('login/', obtain_jwt_token),
    path('', include(router.urls))
]
