# Generated by Django 3.1.4 on 2021-01-03 19:23

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0005_auto_20201214_1708'),
        ('order', '0003_auto_20210103_0935'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='customer',
        ),
        migrations.AddField(
            model_name='orderproduct',
            name='customer',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, to='agents.customer'),
            preserve_default=False,
        ),
    ]