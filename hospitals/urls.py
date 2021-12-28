from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('?', views.filters, name='filter'),
    path('kb/', views.kb, name='knowledge_box'),
]
