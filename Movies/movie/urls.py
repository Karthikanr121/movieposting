from django.urls import path
from . import views
urlpatterns = [
    path('', views.movie_list, name='movie_list'),
    path('movie/<int:pk>/', views.movie_detail, name='movie_detail'),
    path('category/<int:category_id>/', views.category_movies, name='category_movies'),
    path('add_movie/', views.add_movie, name='add_movie'),
    path('register',views.register,name='register'),
    path('login',views.login,name='login'),
    path('logout',views.logout,name='logout'),
    path('delete_movie/<int:pk>/', views.delete_movie, name='delete_movie'),
    path('update_movie/<int:pk>/',views.update_movie,name='update_movie'),
    path('view_profile/', views.view_profile, name='view_profile'),
    path('/<int:movie_id>/add_comment/',views.add_comment,name='add_comment'),
    path('/<int:movie_id>/add_rating/',views.add_rating,name='add_rating'),
    ]