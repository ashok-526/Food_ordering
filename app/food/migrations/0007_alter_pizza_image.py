# Generated by Django 5.1.4 on 2024-12-26 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('food', '0006_remove_orderplace_payment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pizza',
            name='image',
            field=models.ImageField(upload_to='pizzas'),
        ),
    ]