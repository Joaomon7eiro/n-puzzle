from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('solve_puzzle/', views.solve_puzzle, name='solve_puzzle'),
]