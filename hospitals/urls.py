from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('infographics', views.infographics, name='infographics'),
    path('?', views.filters, name='filter'),
    path('kb/', views.kb, name='knowledge_box'),
    path('cities-dbpedia', views.cities_dbpedia, name='cities-dbp'),
    path('counties-dbpedia', views.counties_dbpedia, name='counties-dbp'),
]
