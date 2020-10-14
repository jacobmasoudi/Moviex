from django.urls import path
from . import views

app_name = 'movies'
urlpatterns = [
    path('', views.log, name='log'),
    path('register', views.register, name="register"),
    path('login', views.login, name="login"),
    path('loginform', views.loginform, name="loginform"),
    path('logout', views.logout, name="logout"),
    # ---------------------------------------------------------------------------
    path('index', views.index, name='index'),
    path('result', views.result, name='result'),
    path('movieDetail', views.movieDetail, name='movieDetail'),
    path('add_movie', views.add_movie, name='add_movie'),
    path('<int:movie_id>', views.delete_movie, name='delete_movie'),
    path('edit_movie/<int:movie_id>', views.edit_movie, name='edit_movie'),
    path('update_movie/<int:movie_id>', views.update_movie, name='update_movie'),
    path('dashboard', views.dashboard, name='dashboard'),

]
