
from django.urls import path
from . import views
app_name = 'app'

urlpatterns=[
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('include',views.include,name='include'),
    path('detail',views.detail,name='detail'),
    path('logout',views.logout,name='logout'),
    path('include_file',views.include_file,name='include_file')
]