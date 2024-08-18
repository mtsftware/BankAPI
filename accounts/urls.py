from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.UserDetailView, name='user-detail'),
    path('profile/my_accounts/', views.AccountListCreateView, name='account-list-create'),
    path('profile/my_accounts/<int:account_id>/', views.AccountDetailView, name='account-detail'),
    path('profile/my_accounts/<int:account_id>/transfer', views.TransferView, name='transfer'),
    path('profile/my_accounts/<int:account_id>/dw', views.DepositAndWithdrawView, name='dw')
]