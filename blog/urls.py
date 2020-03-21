from django.urls import path
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/new/', views.post_new, name='post_new'),
    path('post/<int:pk>/edit/', views.post_edit, name='post_edit'),
    # path('user_login/',views.user_login,name='user_login'),
    path('signup/', views.signup, name='signup'),
    path('post_upvote/<int:pk>/', views.post_upvote, name='post_upvote'),
]