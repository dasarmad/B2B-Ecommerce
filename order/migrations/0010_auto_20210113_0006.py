# Generated by Django 3.1.4 on 2021-01-13 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0009_auto_20210112_2351'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='code',
            field=models.CharField(editable=False, max_length=10),
        ),
    ]