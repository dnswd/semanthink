from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('infographics', views.infographics, name='infographics'),
    path('?', views.filters, name='filter'),
    path('kb/', views.kb, name='knowledge_box'),
]
