from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserCreateView, name='user-create'),
    path('<int:id>/', views.UserDetailView, name='user-detail'),
    path('<int:user_id>/my_accounts/', views.AccountListCreateView, name='account-list-create'),
    path('<int:user_id>/my_accounts/<int:account_id>/', views.AccountDetailView, name='account-detail'),
    path('<int:user_id>/my_accounts/<int:account_id>/transfer', views.TransferView, name='transfer'),
    path('<int:user_id>/my_accounts/<int:account_id>/dw', views.DepositAndWithdrawView, name='dw'),
    path('login/', views.login_view, name='login'),
]