# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0003_cart_subtotal'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='tax_percentage',
            field=models.DecimalField(max_digits=10, decimal_places=5, default=0.085),
        ),
        migrations.AddField(
            model_name='cart',
            name='tax_total',
            field=models.DecimalField(max_digits=50, decimal_places=2, default=25.0),
        ),
        migrations.AddField(
            model_name='cart',
            name='total',
            field=models.DecimalField(max_digits=50, decimal_places=2, default=25.0),
        ),
    ]
