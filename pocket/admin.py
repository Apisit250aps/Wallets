from django.contrib import admin

from . import models
# Register your models here.

@admin.register(models.Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'desc',
        'created_at',
        'updated_at',
    ]
    
@admin.register(models.Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = [
        'name',
        'type',
        'amount',
        'wallet'
    ]