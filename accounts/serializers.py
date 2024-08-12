from datetime import timezone
from django.contrib.auth.hashers import make_password
from rest_framework import serializers
from .models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password', 'first_name', 'last_name', 'email',
                  'identity_no', 'phone_number', 'customer_no', 'created_at', 'updated_at')
        read_only_fields = ('customer_no','created_at', 'updated_at')
        extra_kwargs = {'password': {'write_only': True, 'required':True, 'max_length': 6}}

    def validate_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError('Password must be at least 6 characters')
        if not value.isdigit():
            raise serializers.ValidationError('Password must contain only digits')
        return value

    def validate_identity_no(self, value):
        if len(value) != 11 or not value.isdigit() or str(value)[0] == '0':
            raise serializers.ValidationError('Invalid identity number')

        digits = list(map(int, value))

        total1 = sum(digits[0:10:2])
        total2 = sum(digits[1:9:2])
        check1 = (total1 * 7 - total2) % 10
        check2 = (total1 + total2 + check1) % 10
        if check1 == digits[9] and check2 == digits[10]:
            return value
        else:
            raise serializers.ValidationError('Invalid identity number')

    def validate_phone_number(self, value):
        def phone_validate(phone_number, file_path):
            if len(phone_number) == 10 and phone_number.isdigit():
                try:
                    with open(file_path, 'r') as file:
                        code = file.read().splitlines()
                    phone_code = str(phone_number)[:3]
                    if phone_code in code:
                        return True
                except:
                    return False
            return False
        if phone_validate(value, 'phoneValidate.txt'):
            return value
        else:
            raise serializers.ValidationError('Invalid phone number')


    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(UserSerializer, self).create(validated_data)

    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.phone_number = validated_data.get('phone_number', instance.phone_number)
        instance.password = make_password(validated_data.get('password', instance.password))
        instance.save()
        return instance

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('account_type', 'account_number', 'iban', 'balance',
                  'created_at', 'updated_at')
        read_only_fields = ('account_number','iban','created_at', 'updated_at')

    def update(self, instance, validated_data):
        instance.account_type = validated_data.get('account_type', instance.account_type)
        instance.balance = validated_data.get('balance', instance.balance)
        instance.save()
        return instance

class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = ['account', 'iban', 'amount', 'description', 'date', 'extract_number']
        read_only_fields = ('account', 'date', 'extract_number')

class DepositAndWithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = DepositAndWithdraw
        fields = ['account', 'types', 'amount', 'extract_number', 'date']
        read_only_fields = ['account', 'extract_number', 'date']