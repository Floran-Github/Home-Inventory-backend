from rest_framework.views import APIView
from rest_framework import permissions,status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from inventoryAPI.models import *
from django.db.models import Q

from inventoryAPI.serializers import *

class InventoryAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,format=None):
        try:
            query = Inventory.objects.filter(Q(user_associated=request.user.id) | Q(sharedTo__id=request.user.id))
            print(query)

            serial = inventorySerializer(query,many=True)

            context = {
                "inventories" : serial.data
            }
            return Response(context,status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message':'Something went wrong'},status=status.HTTP_404_NOT_FOUND)


class InventoryProductAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,pk=None):
        try:
            invCheck = Inventory.objects.filter(Q(user_associated=request.user.id) | Q(sharedTo__id=request.user.id)).get(pk=pk)
            prdName = request.data['prdName']
            prdData = Product.objects.filter(prdName=prdName)

            if prdData:
                return Response(
                    {'message':'bhai idhar aa gai'},status=status.HTTP_200_OK
                )
            else:
                prdDict = {
                    'prdName':request.data['prdName'],
                    'freezerPrd':request.data['freezerPrd'],
                    'readyToEat':request.data['readyToEat'],
                    'product_type':request.data['product_type'],
                    'product_weight_category':request.data['product_weight_category'],

                }

                prdSerializer = productSerializer(data=prdDict)
                if prdSerializer.is_valid():
                    prdSerialData = prdSerializer.save()

                    prdPriceHistoryDict = {
                        'prdAssociated': prdSerialData.pk,
                        'prdPrice':request.data['prdPrice']
                    }

                    prdPriceSerializer = ProductPriceHistorySerializer(data=prdPriceHistoryDict)

                    if prdPriceSerializer.is_valid():
                        prdPriceData = prdPriceSerializer.save()
                    else:
                        prdSerialData.delete()
                        raise ValidationError(prdPriceSerializer.errors)

                    invPrdDict = {
                        'invAssociated':invCheck.pk,
                        'prodAssociated':prdSerialData.pk,
                        'prdQty':request.data['prdQty'],
                        'product_weight_per_quantity':request.data['product_weight_per_quantity'],
                        'totalquantity':request.data['totalquantity'],
                    }

                    invPrdSerial = InventoryProductSerializer(data=invPrdDict)

                    if invPrdSerial.is_valid():
                        invPrdData = invPrdSerial.save()
                    else:
                        prdSerialData.delete()
                        prdPriceData.delete()
                        raise ValidationError(invPrdSerial.errors)
                    
                    context={
                        'message':'Product Created'
                    }

                    return Response(context,status=status.HTTP_201_CREATED)
                else:
                    raise ValidationError(prdSerialData.errors)
        except Exception as e:
            print(e)
            return Response({'message':'something went wrong'},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self,request,pk=None):
      
        try:
            invCheck = Inventory.objects.filter(Q(user_associated=request.user.id) | Q(sharedTo__id=request.user.id)).get(pk=pk)
            products = InventoryProduct.objects.filter(invAssociated=invCheck.pk)

            prdList = []

            for i in products:
                pd = Product.objects.filter(pk=i.prodAssociated.pk)
                pdprice = ProductPriceHistory.objects.filter(prdAssociated=pd[0].pk)             
                pd = pd.values()[0]
                pd['priceHistory'] = pdprice.values()
                prdList.append(pd)

            context = {
                'products': prdList
            }

            return Response(context,status=status.HTTP_200_OK)

            
        except Exception as e:
            print(e)
            return Response({'message':'Inventory not found'},status=status.HTTP_404_NOT_FOUND)

       