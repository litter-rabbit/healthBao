
from django.urls import path
from . import views
app_name = 'app'

urlpatterns=[
    path('',views.index,name='index'),
    path('login',views.login,name='login'),
    path('include',views.include,name='include'),
    path('detail',views.detail,name='detail'),
    path('logout',views.logout,name='logout'),
    path('search',views.search,name='search'),
    path('delete_one',views.delete_one,name='delete_one'),
    path('update_one_status',views.update_one_status,name='update_one_status'),
    path('update_status',views.update_status,name='update_status'),
    path('include_file',views.include_file,name='include_file')
]