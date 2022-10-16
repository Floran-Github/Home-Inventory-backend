from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import *

class TransactionRecordSerializer(ModelSerializer):
    class Meta:
        model = TransactionRecord
        fields = "__all__"

class TransactionItemSerializer(ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = "__all__"
