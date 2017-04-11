from django.db import models
from df_goods.models import GoodsInfo

# Create your models here.


class UserInfo(models.Model):
    uname = models.CharField(max_length=20)
    upwd = models.CharField(max_length=40)
    uemail = models.CharField(max_length=30)
    ureceive_user = models.CharField(max_length=20)
    uaddress = models.CharField(max_length=100, default='')
    postcode = models.CharField(max_length=6, default='')
    ureceive_phone = models.CharField(max_length=11, default='')


class UserView(models.Model):
    uid = models.ForeignKey(UserInfo)
    gid = models.ForeignKey(GoodsInfo)
