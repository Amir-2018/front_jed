from django.urls import path
from . import views

urlpatterns = [
    # get all users
    path('', views.user_list),
    # insert user into database 
    path('insert-user/', views.insert_user),
    path('user_list/', views.user_list),
    path('login-user/', views.login_user),
    path('delete_user/<int:user_id>/', views.delete_user, name='delete_user'),
    path('get_users/', views.get_list_users),
    path('get_users/<int:idemp>/', views.get_user_by_idemp, name="update_user"),
    path('changePass/', views.changePass),
    path('update_user/<int:user_id>/', views.update_user),
    path('update_user_crud/<int:user_id>/', views.update_user_crud),

# Add large object into database 
#    path('add_file/', views.add_file),

    # Your other URL patterns
    path('show_files/', views.show_files, name='show_files'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),


    path('logout/', views.logout),

    




]   