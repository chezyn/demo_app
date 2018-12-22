from django.urls import path
from . import views

# urlの設定
urlpatterns = [
    path('', views.index, name='index'),
    path('input_form', views.input_form, name='input_form'),
    path('result', views.result, name='result'),
    path('calculate', views.calculate, name='calculate')
]
