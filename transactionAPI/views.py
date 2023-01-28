from rest_framework import permissions,status
from rest_framework.views import APIView
from .models import *
from .serilaizers import *
from inventoryAPI.serializers import *
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError

from django.db.models import Q

class UserTransactionsListViewAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self,request,format=None):
        try:
            transData = TransactionRecord.objects.filter(user_associated=request.user).values()
            context = {
                
            }

            return Response(transData,status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'message':e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InventoryTransaction(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk):

        transData = TransactionRecord.objects.filter(invAssociated=pk)
        transItem = TransactionItem.objects.filter(transactionAssociated=transData.pk)
        data = []

        for i in transItem:
            prd = Product.objects.filter(pk=i.prdAssociated.pk).values()[0]
            invPrd = InventoryProduct.objects.get(invAssociated=inv,prodAssociated=prd['id'])
            prdPriceHistory = ProductPriceHistory.objects.filter(prdAssociated=prd['id']).values()
            prd['prdQty'] = invPrd.prdQty
            prd['product_weight_per_quantity'] = invPrd.product_weight_per_quantity
            prd['totalquantity'] = invPrd.totalquantity
            prd['priceHistory'] = prdPriceHistory

            data.append(prd)

        context = {
            "market": transData.marketAssocaited,
            "transDate": transData.transDate,
            "totalAmount": transData.totalAmount,
            "totalItem": transData.totalItem,
            "prodcuts": data
        }

        return Response(context,status=status.HTTP_200_OK)

class UserTransactionsDetailViewAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,pk=None):
        try:
            try:
                data = []
                transData = TransactionRecord.objects.get(Q(invAssociated__user_associated=request.user.id) | Q(invAssociated__sharedTo__id=request.user.id),pk=pk)
                print(transData)
                itemData = TransactionItem.objects.filter(transactionAssociated=transData)
                inv = transData.invAssociated

                for i in itemData:
                    prd = Product.objects.filter(pk=i.prdAssociated.pk).values()[0]
                    invPrd = InventoryProduct.objects.get(invAssociated=inv,prodAssociated=prd['id'])
                    prdPriceHistory = ProductPriceHistory.objects.filter(prdAssociated=prd['id']).values()
                    prd['prdQty'] = invPrd.prdQty
                    prd['product_weight_per_quantity'] = invPrd.product_weight_per_quantity
                    prd['totalquantity'] = invPrd.totalquantity
                    prd['priceHistory'] = prdPriceHistory

                    data.append(prd)
                
                context = {
                    'market': transData.marketAssocaited.name,
                    'transDate':transData.transDate,
                    'totalAmount':transData.totalAmount,
                    'totalItem':transData.totalItem,
                    'products':data
                }
                
                return Response(context,status=status.HTTP_200_OK)
                

            except Exception as e1:
                return Response({'message':str(e1)},status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'message':e},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class TransactionManualCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request,*args,**kwargs):
        try:
            transData = request.data['transData']
        except Exception as e:
            return Response({'message':str(e)},status=status.HTTP_400_BAD_REQUEST)

class TrancsactionOCRCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request,*arg,**kwargs):
        invCheck = Inventory.objects.filter(Q(user_associated=request.user.id) | Q(sharedTo__id=request.user.id),pk=request.data['invAssociated'])
        if len(invCheck) == 0:
            return Response({'msgs':'No inventory found'},status=status.HTTP_400_BAD_REQUEST)

        data = request.data['scannedData']
        market = request.data['market']
        productData = []
        prices = []
        result = []
        print(data)
        print(market)
        data = data.split("\n")
        for i in data:
            if i == "":
                continue
            try:
                price = float(i)
                prices.append(price)
            except:
                k = 0
                for j in i:
                    if j.isdigit():
                        k += 1
                    else:
                        break
                productData.append([i[:k],i[k:]])
        
        print(productData)
        print(prices)

        # product area
        for i in range(len(productData)):
            prd = Product.objects.filter(prdName=productData[i][1])
            if prd:
                # product history
                prdHistorydata = {
                    'prdAssociated': prd[0].pk,
                    'prdPrice':prices[i]
                }

                prdHistorySerial = ProductPriceHistorySerializer(data=prdHistorydata)
                if prdHistorySerial.is_valid():
                    prdHistorysave = prdHistorySerial.save()
                else:
                    raise ValidationError(prdHistorySerial.errors) 

                # checking if product exists in inventory
                invPrd = InventoryProduct.objects.filter(invAssociated=invCheck[0].pk,prodAssociated=prd[0].pk)
                # if exist update the record
                if invPrd:
                    invPrdUpdate = invPrd.get(pk=invPrd[0].pk)
                    invPrdUpdate.prdQty += productData[i][0]
                    invPrdUpdate.product_weight_per_quantity += 1
                    invPrdUpdate.totalquantity += productData[i][0] * 1
                    invPrdUpdate.save()

                else:
                    # or else create it
                    invprddata = {
                        'invAssociated':invCheck[0].pk,
                        'prodAssociated':prd[0].pk,
                        'prdQty': productData[i][0],
                        'product_weight_per_quantity': 1,
                        'totalquantity': productData[i][0] * 1
                    }

                    if invprdserial.is_valid():
                        invprdsave = invprdserial.save()

                    else:
                        raise ValidationError(invprdserial.errors)
                

                

            else:
                # creating product
                if productData[i][1] in ('PEAS','MUSHROOMS'):
                    prdCatog = 'kilogram'
                else:
                    prdCatog = 'pieces'

                pdata ={
                    'prdName':productData[i][1],
                    'product_type':'edible',
                    'product_weight_category': prdCatog
                }

                prdSerial = productSerializer(data=pdata)

                if prdSerial.is_valid():
                    prdSave = prdSerial.save()

                    # product history
                    prdHistorydata = {
                        'prdAssociated': prdSave.pk,
                        'prdPrice':prices[i]
                    }

                    prdHistorySerial = ProductPriceHistorySerializer(data=prdHistorydata)
                    if prdHistorySerial.is_valid():
                        prdHistorysave = prdHistorySerial.save()
                    else:
                        raise ValidationError(prdHistorySerial.errors) 

                    # inventory product part
                    invprddata = {
                        'invAssociated':invCheck[0].pk,
                        'prodAssociated':prdSave.pk,
                        'prdQty': productData[i][0],
                        'product_weight_per_quantity': 1,
                        'totalquantity': productData[i][0] * 1
                    }

                    invprdserial = InventoryProductSerializer(data=invprddata)

                    if invprdserial.is_valid():
                        invprdsave = invprdserial.save()

                    else:
                        raise ValidationError(invprdserial.errors)

                    rs = {
                        'prdName':productData[i][1],
                        'prdQty':productData[i][0],
                        'totalPrice':prices[i],
                        'product_weight_per_quantity':1
                    }
                    result.append(rs)
                else:
                    raise ValidationError(prdSerial.errors)
        
        # # purchase area
        # market = Market.objects.get(name='other')

        # # transactionRecord

        # transData = {
        #     'user_associated':request.user.id,
        #     'marketAssociated':market.pk,
        #     'invAssociated':invCheck[0].pk,
        #     'totalAmount': len(productData),
        #     'totalItem': sum(prices)
        # }

        # transSerial = TransactionRecordSerializer(data=transData)

        # if transSerial.is_valid():
        #     transSave = transSerial.save()

        #     for i in range(len(productData)):
        #         prd = Product.objects.get(prdName=productData[i][1])
        #         transitem = {
        #             'transactionAssociated':transSave.pk,
        #             'prdAssociated':prd.pk,
        #             'prdQty':productData[i][0],
        #             'prdPerPrice': prices[i] / productData[i][0],
        #             'totalPrice':prices[i]
        #         }

        #         transitemSerial = TransactionItemSerializer(data=transitem)

        #         if transitemSerial.is_valid():
        #             transitemSave = transitemSerial.save()
        #         else:
        #             raise ValidationError(transitemSerial.errors)
        # else:
        #     raise ValidationError(transSerial.errors)

        return Response({'recordItems':result,'totalPrice':sum(prices),'transId':1},status=status.HTTP_201_CREATED)