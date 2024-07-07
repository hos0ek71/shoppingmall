# 프로젝트의 urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shoppingmall.urls')),  # 쇼핑몰 앱의 urls를 포함
]

# 쇼핑몰 앱의 urls.py
from django.urls import path
from . import views

app_name = 'shoppingmall'

urlpatterns = [
    path('', views.index, name='index'),
    path('fetch_image/', views.fetch_image, name='fetch_image'),
]
