from django.db import models

# Create your models here.

class Wallet(models.Model):
    name = models.CharField(max_length=255)
    desc = models.CharField(max_length=255)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    
    def __str__(self) -> str:
        return self.name

class Transaction(models.Model):
    wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    type = models.IntegerField(choices=(
        (1, "Income"),
        (-1, "Expenses")
    ))
    date = models.DateTimeField()
    remark = models.TextField(default="-")
    writer = models.CharField(max_length=255, default="admin")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self) -> str:
        return self.name