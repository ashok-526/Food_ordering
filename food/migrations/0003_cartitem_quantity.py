# Generated by Django 4.2.4 on 2023-08-29 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0002_cart_esewa_alter_pizza_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
