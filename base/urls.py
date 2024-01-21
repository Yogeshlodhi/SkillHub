from django.urls import path

from . import views

urlpatterns = [
    path('login/', views.LoginPage ,name="login"),
    path('logout/', views.logoutUser ,name="logout"),
    path('register/', views.registerUser ,name="register"),
    path('',views.Home, name="home"),
    path('room/<str:pk>/',views.Rooms, name="rooms"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('create-room/', views.CreateRoom, name="create-room"),
    path('update-room/<str:pk>/', views.UpdateRoom, name="update-room"),
    path('delete-room/<str:pk>/', views.DeleteRoom, name="delete-room"),
    path('delete-message/<str:pk>/', views.deleteMessage, name="delete-message"),
    path('update-user/', views.updateUser, name="update-user"),
    path('topics/', views.topicsPage, name="topics"),
    path('activity/', views.activityPage, name="activity"),
]