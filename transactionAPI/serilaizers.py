from dataclasses import field
from rest_framework.serializers import ModelSerializer
from .models import *

class TransactionRecordSerializer(ModelSerializer):
    class Meta:
        model = TransactionRecord
        fields = "__all__"

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['marketAssocaited'] = instance.marketAssocaited.name
        rep['invAssociated'] = instance.invAssociated.invName

        return rep
    
class TransactionItemSerializer(ModelSerializer):
    class Meta:
        model = TransactionItem
        fields = "__all__"

    def to_representation(self, instance):
        rep  =super().to_representation(instance)
        
        rep['prdAssociated'] = instance.prdAssociated.prdName

        return rep
