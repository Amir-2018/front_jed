from django.urls import include, path
from django.contrib import admin
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('test/', views.test),
    path('changepass/', views.ChangePass),
    path('consulter/', views.consulter),
    path('smp/', views.consulterSimple),
    path('index/', views.index),
    path('add/', views.adduser),
    path('users/', include('users.urls')),
    path('', views.homepage),
    path('get_first/', views.get_first),
    path('adminUser/', views.admin),
    path('GetListDir/', views.get_list_dir, name='GetListDir'),
   
]
urlpatterns += staticfiles_urlpatterns()