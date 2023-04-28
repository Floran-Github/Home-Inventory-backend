from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from datetime import date


from inventoryAPI.models import *
from django.db.models import Q

from inventoryAPI.serializers import *


class InventoryAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, format=None):
        try:
            query = Inventory.objects.filter(
                Q(user_associated=request.user.id) | Q(sharedTo__id=request.user.id))
            print(query)

            serial = inventorySerializer(query, many=True)

            return Response(serial.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            return Response({'message': 'Something went wrong'}, status=status.HTTP_404_NOT_FOUND)


class ProductDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, pk):
        prd = Product.objects.filter(pk=pk)
        if not prd.exists():
            return Response({'error': "Product Not Found"}, status=status.HTTP_404_NOT_FOUND)

        prdPriceHistory = ProductPriceHistory.objects.filter(
            prdAssociated=prd[0])
        daylist = []
        datapoint = []
        for i in prdPriceHistory:
            daylist.append(i.date)
            datapoint.append(i.prdPrice)

        context = {
            "detail": prd.values()[0],
            "history": {
                'data': datapoint,
                "days": daylist
            }
        }

        return Response(context, status=status.HTTP_200_OK)


class InventoryProductAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk=None):
        try:
            invCheck = Inventory.objects.filter(Q(user_associated=request.user.id) | Q(
                sharedTo__id=request.user.id)).get(pk=pk)
            prdName = request.data['prdName']
            prdData = Product.objects.filter(prdName=prdName)

            if not prdData:
                return Response(
                    {'message': 'error'}, status=status.HTTP_400_BAD_REQUEST
                )
            else:
                prdDict = {
                    'prdName': request.data['prdName'],
                    'freezerPrd': request.data['freezerPrd'],
                    'readyToEat': request.data['readyToEat'],
                    'product_type': request.data['product_type'],
                    'product_weight_category': request.data['product_weight_category'],

                }

                prdSerializer = productSerializer(data=prdDict)
                if prdSerializer.is_valid():
                    prdSerialData = prdSerializer.save()

                    prdPriceHistoryDict = {
                        'prdAssociated': prdSerialData.pk,
                        'prdPrice': request.data['prdPrice']
                    }

                    prdPriceSerializer = ProductPriceHistorySerializer(
                        data=prdPriceHistoryDict)

                    if prdPriceSerializer.is_valid():
                        prdPriceData = prdPriceSerializer.save()
                    else:
                        prdSerialData.delete()
                        raise ValidationError(prdPriceSerializer.errors)

                    invPrdDict = {
                        'invAssociated': invCheck.pk,
                        'prodAssociated': prdSerialData.pk,
                        'prdQty': request.data['prdQty'],
                        'product_weight_per_quantity': request.data['product_weight_per_quantity'],
                        'totalquantity': request.data['totalquantity'],
                    }

                    invPrdSerial = InventoryProductSerializer(data=invPrdDict)

                    if invPrdSerial.is_valid():
                        invPrdData = invPrdSerial.save()
                    else:
                        prdSerialData.delete()
                        prdPriceData.delete()
                        raise ValidationError(invPrdSerial.errors)

                    context = {
                        'message': 'Product Created'
                    }

                    return Response(context, status=status.HTTP_201_CREATED)
                else:
                    raise ValidationError(prdSerialData.errors)
        except Exception as e:
            print(e)
            return Response({'message': 'something went wrong'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, pk=None):

        invCheck = Inventory.objects.filter(
            Q(user_associated=request.user.id) | Q(sharedTo__id=request.user.id), pk=pk)

        if not invCheck:
            return Response({'message': 'Inventory not found'}, status=status.HTTP_404_NOT_FOUND)

        products = InventoryProduct.objects.filter(
            invAssociated=invCheck[0].pk)

        # serializer
        invSerialize = inventorySerializer(invCheck, many=True)
        prdSerialize = InventoryProductSerializer(products, many=True)

        context = {
            'invdetail': invSerialize.data[0],
            'prdList': prdSerialize.data
        }

        return Response(context, status=status.HTTP_200_OK)
