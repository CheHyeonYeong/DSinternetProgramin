"""myInternetPrj URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('blog/', include('blog.urls')),  # 서버 ip/blog
    path('admin/', admin.site.urls),  # 서버 ip/admin
    path('', include('single_pages.urls')),  # 서버 ip/
    path('markdownx/', include('markdownx.urls')),
    path('accounts/', include('allauth.urls')),
]
#url 생성 fbv 더보기
#python manage.py makemigrations
#python manage.py migrate
#데베에 적용


#헤더 이미지 하는거 요 아래것
urlpatterns+= static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)     #서버IP/MEDIA