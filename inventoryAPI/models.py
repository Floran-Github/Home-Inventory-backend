from django.db import models
from django.contrib.auth.models import User

 
class Inventory(models.Model):
    user_associated = models.ForeignKey(User,on_delete=models.CASCADE)
    invName = models.CharField(max_length=20)
    invCreateDate = models.DateField(auto_now=True)
    sharedTo = models.ManyToManyField(User,related_name='shared',default=None,null=True,blank=True)

    def __str__(self) -> str:
        return self.invName
    
class Product(models.Model):
    PRODUCT_TYPE = [
        ('edible','Edible'),
        ('non-edible','Non-Edible')
    ]

    PRODUCT_WEIGHT_CATEGORY = [
        ('kilogram','Kilogram'),
        ('gram','Gram'),
        ('litre','Litre'),
        ('ml','Mili Litre'),
        ('pieces','Pieces'),
    ]

    prdName = models.CharField(max_length=80)
    freezerPrd = models.BooleanField(default=False)
    readyToEat = models.BooleanField(default=True)
    product_type = models.CharField(max_length=10,choices=PRODUCT_TYPE,default='edible')
    product_weight_category = models.CharField(max_length=10,choices=PRODUCT_WEIGHT_CATEGORY,default='kilogram')

    def __str__(self) -> str:
        return self.prdName

class ProductPriceHistory(models.Model):
    prdAssociated = models.ForeignKey(Product,on_delete=models.CASCADE)
    prdPrice = models.FloatField() 
    date = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.prdAssociated} - price history - {self.pk}'

class InventoryProduct(models.Model):
    invAssociated = models.ForeignKey(Inventory,on_delete=models.CASCADE)
    prodAssociated = models.ForeignKey(Product,on_delete=models.CASCADE)
    prdQty = models.IntegerField()
    product_weight_per_quantity = models.IntegerField(default=0)
    totalquantity = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f'{self.invAssociated} - {self.prodAssociated}'
