# Generated by Django 4.1 on 2022-08-27 19:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customer", "0003_alter_customer_email"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customer",
            name="email",
            field=models.EmailField(
                default="anonim@ecommerce.com",
                max_length=255,
                unique=True,
                verbose_name="email address",
            ),
        ),
    ]
