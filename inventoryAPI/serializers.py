from dataclasses import field
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import *

class inventorySerializer(ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class productSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class InventoryProductSerializer(ModelSerializer):
    class Meta:
        model = InventoryProduct
        fields = '__all__'

class ProductPriceHistorySerializer(ModelSerializer):
    class Meta:
        model = ProductPriceHistory
        fields = '__all__'