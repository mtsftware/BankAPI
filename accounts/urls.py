from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserListCreateView, name='user-list-create'),
    path('<int:id>/', views.UserDetailView, name='user-detail'),
]