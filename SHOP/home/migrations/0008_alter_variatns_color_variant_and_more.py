# Generated by Django 4.1.4 on 2023-01-04 13:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_color_size_product_status_variatns'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variatns',
            name='color_variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.color'),
        ),
        migrations.AlterField(
            model_name='variatns',
            name='size_variant',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='home.size'),
        ),
    ]
