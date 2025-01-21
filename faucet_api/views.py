from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from .models import FundTransaction
from .serializers import FundTransactionSerializer
from .utils import get_client_ip, wei_to_eth
from faucet.settings import APP_SETTINGS
from .web3 import get_transaction, send_transaction, is_address_valid
import json
import logging
from datetime import datetime, timedelta
from .models import FundTransaction

def error_obj(message):
    return {
        'details': message
    } 

class FundApiView(APIView):
    def _is_allowed(self, ip):
        time_before = datetime.now() - timedelta(seconds=APP_SETTINGS['FUND_TIMEOUT'])
        last_transaction = FundTransaction.objects.filter(ip=ip, created__gt=time_before).order_by('-created')
        return not last_transaction
    
    def post(self, request, *args, **kwargs):
        client_ip = get_client_ip(request)
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError as e:
            return JsonResponse(error_obj("invalid input data, expected the receiver_addr key"), status=status.HTTP_400_BAD_REQUEST)
        
        if not self._is_allowed(client_ip):
            return JsonResponse(error_obj("You can faucet address once every %d seconds" % APP_SETTINGS['FUND_TIMEOUT']), status=status.HTTP_403_FORBIDDEN)
        
        if not 'receiver_addr' in data or not is_address_valid(data['receiver_addr']):
            return JsonResponse(error_obj('The receiver address is invalid'), status=status.HTTP_400_BAD_REQUEST)
        
        logging.info("Preparing transaction")
        tx = get_transaction(APP_SETTINGS['WHALE_PRIVATE_KEY'], APP_SETTINGS['FUND_AMOUNT_WEI'], data['receiver_addr'])
        logging.info("Transaction prepared %s" % tx.hash.to_0x_hex())
        
        data = {
            'tx_id': tx.hash.to_0x_hex(), 
            'ip': client_ip, 
            'amount': 0.1,
        }
        serializer = FundTransactionSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        logging.info("Saving transaction %s" % tx.hash.to_0x_hex())
        serializer.save()

        logging.info("Sending transaction %s" % tx.hash.to_0x_hex())
        try:
            receipt = send_transaction(tx)
        except Exception as e:
            return JsonResponse(error_obj(str(e)), status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        logging.info("Updating transaction %s" % tx.hash.to_0x_hex())
        FundTransaction.objects.filter(tx_id=tx.hash.to_0x_hex()).update(completed = datetime.now())
        
        return JsonResponse({
            'tx_hash': receipt.transactionHash.to_0x_hex()
        }, status=status.HTTP_201_CREATED)

class StatsApiView(APIView):
    def get(self, request, *args, **kwargs):
        all_txs = FundTransaction.objects.count()
        successful_txs = FundTransaction.objects.exclude(completed__isnull=True).count()
        
        response = {
            'successful_txs': successful_txs,
            'failed_txs': all_txs-successful_txs,
        }
        return JsonResponse(response)

class EnvironmentApiView(APIView):
    def get(self, request, *args, **kwargs):
        response = {
            'RPC_ADDRESS': "%s..." % APP_SETTINGS['RPC_ADDRESS'][:6],
            'FUND_TIMEOUT': APP_SETTINGS['FUND_TIMEOUT'],
            'FUND_AMOUNT_WEI': wei_to_eth(APP_SETTINGS['FUND_AMOUNT_WEI']),
            'WHALE_PRIVATE_KEY': "%s..." % APP_SETTINGS['WHALE_PRIVATE_KEY'][:6],
        }
        return JsonResponse(response)
