from django.urls import path
from . import views

urlpatterns = [  # 서버ip/blog/
    path('<int:pk>/', views.single_post_page),
    path('', views.index),  # 서버 ip/blog
]
