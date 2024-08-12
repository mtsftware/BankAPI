from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from accounts.models import User, Account
from accounts.serializers import UserSerializer, AccountSerializer


@api_view(['GET', 'POST'])
def UserListCreateView(request):
    if request.method == 'GET':
        users = User.objects.all()  #Books? :)
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
@api_view(['GET', 'PUT', 'DELETE'])
def UserDetailView(request, id):
    if request.method == 'GET':
        try:
            user = User.objects.get(pk=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        user = User.objects.get(pk=id)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
@api_view(['GET', 'POST'])
def AccountListCreateView(request, user_id):
    try:
        user = User.objects.get(pk=user_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        try:
            accounts = Account.objects.filter(user=user)
            serializer = AccountSerializer(accounts, many=True)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'POST':
        serializer = AccountSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def AccountDetailView(request, user_id, id):
    try:
        user = User.objects.get(pk=user_id)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        try:
            account = Account.objects.get(pk=id)
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        account = Account.objects.get(pk=id)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        account = Account.objects.get(pk=id)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)




# Create your views here.
