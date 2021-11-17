from django.urls import path, include
from . import views

urlpatterns = [  # 서버 ip/blog/
    #    path('<int:pk>/', views.single_post_page),
    #    path('', views.index),  # 서버 ip/blog
    path('update_post/<int:pk>/', views.PostUpdate.as_view()),
    path('create_post/', views.PostCreate.as_view()),
    path('tag/<str:slug>', views.tag_page),
    path('category/<str:slug>', views.category_page),
    path('<int:pk>/', views.PostDetail.as_view()),  # pk로 인덱싱 가능 blog에 있음

    path('', views.PostList.as_view()),
]
