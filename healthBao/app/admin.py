from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import  User,Student

class UserAdmin(admin.ModelAdmin):
    list_display = ('username','timestamp')


class StudentAdmin(admin.ModelAdmin):
    list_display = ('name','id_card','status','update_time')

admin.site.site_header = '健康宝管理后台'
admin.site.register(User,UserAdmin)
admin.site.register(Student,StudentAdmin)