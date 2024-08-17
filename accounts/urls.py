from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('register', views.register_view, name='register'),
    path('test_token', views.test_token_view, name='test-token'),
    path('<int:identity_no>/', views.UserDetailView, name='user-detail'),
    path('<int:identity_no>/my_accounts/', views.AccountListCreateView, name='account-list-create'),
    path('<int:identiy_no>/my_accounts/<int:account_id>/', views.AccountDetailView, name='account-detail'),
    path('<int:identity_no>/my_accounts/<int:account_id>/transfer', views.TransferView, name='transfer'),
    path('<int:identity_no>/my_accounts/<int:account_id>/dw', views.DepositAndWithdrawView, name='dw')
]