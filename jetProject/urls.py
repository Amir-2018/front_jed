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
    path('exist/', views.exist),

    path('ajouter_titre/', views.testgvs3),

    #path('GetListDir/', views.get_list_dir, name='GetListDir'),
    path('export_and_show/', views.export_and_show_file, name='export_and_show'),
    path('if_exist/', views.GetTitreExiste),
    #path('insert_data/', views.insert_data),
    path('get_list_gouv/', views.testgvs),
    path('test_exist_in_tfich/', views.test_exist_in_tfich),
    path('insert_data/', views.data_insert, name='data_insert'),
    path('exist_titre_ged/',views.tester_titre_existance),
    # import multiple files in titreimages table 
    path('import_files_with_codetitre/',views.test_import),
    path('display_images/',views.display_images_from_tempd),
    #path('uptest/',views.uptest)
    #path('del_All/',views.del_All)
    path('find_dell/',views.find_dell),
    path('get_count/',views.get_count_titresimages)




]
urlpatterns += staticfiles_urlpatterns()