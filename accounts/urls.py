from django.urls import path
from . import views

urlpatterns = [
    path('', views.UserCreateView, name='user-create'),
    path('<int:identiy_no>/', views.UserDetailView, name='user-detail'),
    path('<int:identity_no>/my_accounts/', views.AccountListCreateView, name='account-list-create'),
    path('<int:identiy_no>/my_accounts/<int:account_id>/', views.AccountDetailView, name='account-detail'),
    path('<int:identity_no>/my_accounts/<int:account_id>/transfer', views.TransferView, name='transfer'),
    path('<int:identity_no>/my_accounts/<int:account_id>/dw', views.DepositAndWithdrawView, name='dw'),
    path('login', views.login_view, name='login'),
]