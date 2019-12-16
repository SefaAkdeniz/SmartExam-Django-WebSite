from django.urls import path
from . import views

urlpatterns = [
    path('',views.index, name='exam'),
    path('stat/',views.stat, name='stat')
]