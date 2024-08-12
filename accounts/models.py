from django.contrib.auth.models import AbstractUser, Permission, Group
from django.db import models
import random as rnd
class User(AbstractUser):
    email = models.EmailField(unique=True, null=False)
    first_name = models.CharField(max_length=50, null=False)
    last_name = models.CharField(max_length=50, null=False)
    identity_no = models.CharField(max_length=11, unique=True, null=False)
    phone_number = models.CharField(max_length=10, unique=True, null=False)
    customer_no = models.CharField(max_length=9, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        related_query_name='user',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        related_query_name='user',
    )
    def __str__(self):
        return f"{self.identity_no}"

    def save(self, *args, **kwargs):
        if not self.customer_no:
            self.customer_no = rnd.randint(100000000, 999999999)
            while User.objects.filter(customer_no=self.customer_no).exists():
                self.customer_no = rnd.randint(100000000, 999999999)
        super().save(*args, **kwargs)



class Account(models.Model):
    ACCOUNT_TYPES = [
        ('non_term', 'Non-Term'),
        ('term', 'Term')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='non_term')
    account_number = models.CharField(max_length=15, unique=True, blank=True)
    iban = models.CharField(max_length=26, unique=True, blank=True)
    balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.account_number} - {self.get_account_type_display()}"

    def save(self, *args, **kwargs):
        def iban_create():
            while True:
                iban_num='TR'+''.join([str(rnd.randint(0,9)) for _ in range(24)])
                if not Account.objects.filter(iban=iban_num).exists():
                    return iban_num
        def account_number_create():
            while True:
                account_num=''.join([str(rnd.randint(0,9)) for _ in range(15)])
                if not Account.objects.filter(account_number=account_num).exists():
                    return account_num
        if not self.iban:
            self.iban = iban_create()
        if not self.account_number:
            self.account_number = account_number_create()
        super().save(*args, **kwargs)

class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit','Deposit'),
        ('withdrawal', 'Withdrawal'),
        ('transfer','Transfer'),
        ('payment','Payment'),
    ]

    account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(unique=True, max_length=20, blank=True)

    def __str__(self):
        return f"{self.reference} - {self.date}"

    def save(self, *args, **kwargs):
        def reference_create():
            while True:
                reference_num = ''.join([str(rnd.randint(0,9)) for _ in range(30)])
                if not Transaction.objects.filter(reference=reference_num).exists():
                    return reference_num

        self.reference = reference_create()
        super().save(*args, **kwargs)