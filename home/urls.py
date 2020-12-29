from django.urls import path

from home import views

app_name = 'home'
urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.Login_user.as_view(), name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.Register_user.as_view(), name='register'),
    path('profile/<str:username>', views.Profile.as_view(), name='profile'),
    path('profile/', views.index),
    path('profile/update/avatar', views.Update.as_view(), name='update'),
    path('timkiem/', views.Timkiem.as_view(), name='timkiem'),
    # path('chat/<int:user_2_id>', views.box_chat.as_view(), name='chat'),
    path('chat/api/<int:user_2_id>', views.api_ajax.as_view(), name='api'),

]
