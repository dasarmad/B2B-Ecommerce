# Generated by Django 3.1.4 on 2021-01-12 23:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_auto_20201214_1708'),
        ('order', '0008_auto_20210112_2350'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orderproduct',
            name='customer',
            field=models.ForeignKey(default=0, max_length=1000, null=True, on_delete=django.db.models.deletion.CASCADE, to='agents.customer'),
        ),
    ]
