from django.urls import path
from app import views
urlpatterns = [
    path('gcal/', views.main),
    path('api/', views.api),
    path('', views.api),
]
