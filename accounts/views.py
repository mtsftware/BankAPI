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

    token = Token.objects.get(user=user)
    serializer = UserLoginSerializer(instance=user)
    data = serializer.data
    data['token'] = token.key
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET'])
@authentication_classes((TokenAuthentication, SessionAuthentication))
@permission_classes([IsAuthenticated])
def test_token_view(request):
    return Response("passed for {}".format(request.user.first_name))


@api_view(['GET', 'PUT', 'DELETE'])
def UserDetailView(request, identity_no):
    if request.method == 'GET':
        try:
            user = User.objects.get(identity_no=identity_no)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'PUT':
        user = User.objects.get(identity_no=identity_no)
        serializer = UserSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'DELETE':
        user = User.objects.get(identity_no=identity_no)
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
def AccountListCreateView(request, identity_no):
    try:
        user = User.objects.get(identity_no=identity_no)
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
def AccountDetailView(request, identity_no, account_id):
    if request.method == 'GET':
        try:
            user = User.objects.get(identity_no=identity_no)
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
def TransferView(request, identity_no, account_id):
    try:
        user = User.objects.get(identity_no=identity_no)
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
def DepositAndWithdrawView(request, identity_no, account_id):
    try:
        user = User.objects.get(identity_no=identity_no)
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
