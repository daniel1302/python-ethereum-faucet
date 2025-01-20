from django.db import models

class FundTransaction(models.Model):
    tx_id = models.CharField(max_length=70, primary_key=True, blank = True)
    ip = models.CharField(max_length = 15)
    amount = models.DecimalField(max_digits=26, decimal_places=18, blank=False)
    created = models.DateTimeField(auto_now_add = True, auto_now = False, blank = False)
    completed = models.DateTimeField(blank = True)

    def __str__(self):
        return self.tx_id

    class Meta:
        default_permissions = ()