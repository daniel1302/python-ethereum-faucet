# todo/todo_api/serializers.py
from rest_framework import serializers
from .models import FundTransaction
class FundTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundTransaction
        fields = ["tx_id", "ip", "amount", "created", "completed"]