from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('procesar', views.procesar),
    path('verdoc/', views.verdoc, name="verdoc")
]
