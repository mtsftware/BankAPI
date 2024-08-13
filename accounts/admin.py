from django.contrib import admin
from .models import User, Account, Transfer, DepositAndWithdraw

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'identity_no', 'phone_number', 'customer_no', 'created_at', 'updated_at')
    search_fields = ('username', 'email', 'identity_no', 'phone_number')
    list_filter = ('created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('username', 'first_name', 'last_name', 'email', 'identity_no', 'phone_number', 'customer_no')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_number', 'iban', 'user', 'account_type', 'balance', 'created_at', 'updated_at')
    search_fields = ('account_number', 'iban', 'user__username')
    list_filter = ('account_type', 'created_at', 'updated_at')
    readonly_fields = ('iban', 'account_number', 'created_at', 'updated_at')
    ordering = ('-created_at',)
    fieldsets = (
        (None, {
            'fields': ('user', 'account_type', 'account_number', 'iban', 'balance')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ('extract_number', 'account', 'iban', 'amount', 'description', 'date')
    search_fields = ('extract_number', 'account__account_number', 'iban')
    list_filter = ('date',)
    readonly_fields = ('extract_number', 'date')
    ordering = ('-date',)
    fieldsets = (
        (None, {
            'fields': ('account', 'iban', 'amount', 'description')
        }),
        ('Extract Details', {
            'fields': ('extract_number', 'date'),
            'classes': ('collapse',),
        }),
    )

@admin.register(DepositAndWithdraw)
class DepositAndWithdrawAdmin(admin.ModelAdmin):
    list_display = ('extract_number', 'account', 'types', 'amount', 'date')
    search_fields = ('extract_number', 'account__account_number')
    list_filter = ('types', 'date')
    readonly_fields = ('extract_number', 'date')
    ordering = ('-date',)
    fieldsets = (
        (None, {
            'fields': ('account', 'types', 'amount')
        }),
        ('Extract Details', {
            'fields': ('extract_number', 'date'),
            'classes': ('collapse',),
        }),
    )



# Register your models here.
