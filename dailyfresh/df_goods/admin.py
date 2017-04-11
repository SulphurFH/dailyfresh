from django.contrib import admin
from .models import *

# Register your models here.


class GoodsInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'gtitle', 'gpic', 'gprice',
                    'isDelete', 'gunit', 'gjianjie', 'gkucun', 'gcontent']


class TypeInfoAdmin(admin.ModelAdmin):
    list_per_page = 10
    list_display = ['id', 'ttitle']


admin.site.register(GoodsInfo, GoodsInfoAdmin)
admin.site.register(TypeInfo, TypeInfoAdmin)
