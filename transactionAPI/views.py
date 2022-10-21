from rest_framework import permissions,status
from rest_framework.views import APIView
from .models import *
from rest_framework.response import Response
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
        data = request.data['scannedData']

        print(data)

        return Response({'message':'data'},status=status.HTTP_200_OK)