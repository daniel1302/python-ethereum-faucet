from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import FundTransaction
from .serializers import FundTransactionSerializer
from .utils import get_client_ip

class FundApiView(APIView):
    def post(self, request, *args, **kwargs):
        
        data = {
            'tx_id': '...', 
            'ip': get_client_ip(request), 
            'amount': 0.1,
        }
        serializer = FundTransactionSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StatsApiView(APIView):
    def get(self, request, *args, **kwargs):
        response = {
            'successful_txs': 10,
            'failed_txs': 5,
        }
        return JsonResponse(response)

