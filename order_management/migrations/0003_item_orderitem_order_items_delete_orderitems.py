# Generated by Django 5.1.6 on 2025-02-12 17:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_management', '0002_alter_order_options_order_created_at_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Name of dish')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Price')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1, verbose_name='Quantity')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.item')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order_management.order')),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(through='order_management.OrderItem', to='order_management.item'),
        ),
        migrations.DeleteModel(
            name='OrderItems',
        ),
    ]
