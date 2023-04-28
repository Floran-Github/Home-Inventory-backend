from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import *

class inventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


    def to_representation(self, instance):
        rep =  super().to_representation(instance)
        rep['user_associated'] = instance.user_associated.username

        return rep

class productSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InventoryProductSerializer(ModelSerializer):
    class Meta:
        model = InventoryProduct
        fields = '__all__'

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['prodAssociated'] = productSerializer(instance.prodAssociated).data

        return rep

class ProductPriceHistorySerializer(ModelSerializer):
    class Meta:
        model = ProductPriceHistory
        fields = '__all__'