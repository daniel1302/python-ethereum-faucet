# Generated by Django 5.1.5 on 2025-01-20 19:53

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="FundTransaction",
            fields=[
                (
                    "tx_id",
                    models.CharField(
                        blank=True, max_length=70, primary_key=True, serialize=False
                    ),
                ),
                ("ip", models.CharField(max_length=15)),
                ("amount", models.DecimalField(decimal_places=18, max_digits=26)),
                ("created", models.DateTimeField(auto_now_add=True)),
                ("completed", models.DateTimeField(blank=True)),
            ],
        ),
    ]
