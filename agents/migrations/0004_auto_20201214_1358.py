# Generated by Django 3.1.1 on 2020-12-14 13:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('agents', '0003_auto_20201213_1926'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='productsize',
            name='product',
        ),
        migrations.RemoveField(
            model_name='productsize',
            name='size',
        ),
        migrations.DeleteModel(
            name='ProductColor',
        ),
        migrations.DeleteModel(
            name='ProductSize',
        ),
    ]