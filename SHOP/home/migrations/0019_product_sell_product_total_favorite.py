# Generated by Django 4.1.4 on 2023-02-01 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0018_brand_product_brand_variatns_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sell',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='product',
            name='total_favorite',
            field=models.IntegerField(default=0),
        ),
    ]
