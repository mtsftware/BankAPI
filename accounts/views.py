from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from accounts.models import User, Account
from accounts.serializers import UserSerializer, AccountSerializer, TransferSerializer, DepositAndWithdrawSerializer, \
    UserLoginSerializer


@api_view(['POST'])
def register_view(request):
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def login_view(request):
    user = authenticate(request, identity_no=request.data['identity_no'], password=request.data['password'])
    if user is None:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

    token, create = Token.objects.get_or_create(user=user)
    serializer = UserLoginSerializer(instance=user)
    data = serializer.data
    data['token'] = token.key
    return Response(data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes([IsAuthenticated])
def logout_view(request):
    if request.method == 'GET':
        try:
            request.user.auth_token.delete()
            return Response("Logged out successfully", status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE', 'PATCH'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes([IsAuthenticated])
def UserDetailView(request):
    if request.method == 'GET':
        try:
            user = request.user
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        user = request.user
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        user = request.user
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    if request.method == 'PATCH':
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes([IsAuthenticated])
def AccountListCreateView(request):
    try:
        user =request.user
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
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes([IsAuthenticated])
def AccountDetailView(request, account_id):
    if request.method == 'GET':
        try:
            user = request.user
            account = Account.objects.get(pk=account_id)
            serializer = AccountSerializer(account)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        account = Account.objects.get(pk=account_id)
        serializer = AccountSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        account = Account.objects.get(pk=account_id)
        account.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes([IsAuthenticated])
def TransferView(request, account_id):
    try:
        user = request.user
        main_account = Account.objects.get(pk=account_id)
    except User.DoesNotExist or Account.DoesNotExist:
        return Response({'detail': 'User or account not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            transfer_amount = serializer.validated_data.get('amount')
            if main_account.balance >= transfer_amount:
                main_account.balance -= transfer_amount
                iban = serializer.validated_data.get('iban')
                try:
                    target_account = Account.objects.get(iban=iban)
                    target_account.balance += transfer_amount
                    main_account.save()
                    target_account.save()
                    serializer.save(account=main_account)
                    return Response(serializer.data, status=status.HTTP_201_CREATED)
                except Account.DoesNotExist:
                    return Response({'detail': 'Target account not found'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'detail': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes([IsAuthenticated])
def DepositAndWithdrawView(request, account_id):
    try:
        user = request.user
        account = Account.objects.get(pk=account_id)
    except User.DoesNotExist or Account.DoesNotExist:
        return Response({'detail': 'User or account not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'POST':
        serializer = DepositAndWithdrawSerializer(data=request.data)
        if serializer.is_valid():
            type = serializer.validated_data.get('types')
            amount = serializer.validated_data.get('amount')
            control = False
            if type == 'withdraw':
                if account.balance >= amount:
                    account.balance -= amount
                    control = True
            if type == 'deposit':
                account.balance += amount
            if control:
                account.save()
                serializer.save(account=account)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            else:
                return Response({'detail': 'Insufficient balance'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
