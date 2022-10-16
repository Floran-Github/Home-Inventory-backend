from django.db import models
from django.contrib.auth.models import User
from inventoryAPI.models import *

class Market(models.Model):
    name = models.CharField(max_length=10)

    def __str__(self) -> str:
        return self.name

class TransactionRecord(models.Model):
    user_associated = models.ForeignKey(User,on_delete=models.CASCADE)
    marketAssocaited = models.ForeignKey(Market,on_delete=models.CASCADE)
    invAssociated = models.ForeignKey(Inventory,on_delete=models.CASCADE)
    transDate = models.DateField(auto_now=True)
    totalAmount = models.FloatField()
    totalItem = models.IntegerField()

    def __str__(self) -> str:
        return f"{self.marketAssocaited} transaction by {self.user_associated}"

class TransactionItem(models.Model):
    transactionAssociated = models.ForeignKey(TransactionRecord,on_delete=models.CASCADE)
    prdAssociated = models.ForeignKey(Product,on_delete=models.CASCADE)
    prdQty = models.IntegerField()
    prdPerPrice = models.FloatField()
    totalPrice = models.FloatField()

    def __str__(self) -> str:
        return f"{self.transactionAssociated} - item"