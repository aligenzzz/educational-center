# Generated by Django 4.2.8 on 2024-07-23 11:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('api_product', '0004_alter_review_creation_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='creation_date',
            field=models.DateField(default=django.utils.timezone.localdate),
        ),
    ]
