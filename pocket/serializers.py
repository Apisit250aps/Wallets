from rest_framework import serializers

from . import models
class WalletSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = models.Wallet
        fields = '__all__'
        
class TransactionSerializers(serializers.ModelSerializer):
    
    class Meta:
        model = models.Transaction
        fields = '__all__'