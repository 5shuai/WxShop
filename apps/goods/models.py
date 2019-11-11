from datetime import datetime
from django.db import models


# Create your models here.

class GoodsCategory(models.Model):
    """
    商品类别
    """
    name = models.CharField()
    code = models.CharField()
    desc = models.CharField()
    category_type = models.CharField(choices=())
    parent_category = models.ForeignKey("self",null=True,blank=True,verbose_name="父类别")
    is_tab= models.BooleanField(default=False)



class GoodsCategoryBrand(models.Model):
    """
    品牌名
    """
    name = models.CharField()
    desc = models.TextField()
    image = models.ImageField(upload_to="/brand")
    add_time = models.DateTimeField(default=datetime.now, verbose_name="添加时间")
