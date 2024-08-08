from django.urls import path
from . import views

urlpatterns = [
    path('user/<str:pk>/', views.userProfile, name = 'user'),
    path('login/', views.loginPage, name='login'),
    path('register', views.registerUser, name='register' ),
    path('logout/', views.logoutUser, name='log-out'),
    path('', views.home, name='home'),
    path('room_id/<str:pk>/', views.room, name = 'room'),
    path('create-room/', views.create_room, name='create-room'), 
    path('update-room/<str:pk>/', views.updateRoom, name='update'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete'),
    path('delete-comment/<str:pk>/', views.deleteComment, name='delete-comment')

]