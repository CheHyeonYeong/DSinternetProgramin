from django.urls import path
from . import views

urlpatterns = [  # 서버 ip/
    path('', views.landing),
    path('about_me/', views.about_me),
]
