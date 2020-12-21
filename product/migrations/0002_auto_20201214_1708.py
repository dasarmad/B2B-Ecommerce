# Generated by Django 3.1.1 on 2020-12-14 17:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='price',
            new_name='retail_price',
        ),
        migrations.AddField(
            model_name='product',
            name='wholesale_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
        ),
    ]