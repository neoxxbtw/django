# Generated by Django 5.2 on 2025-05-22 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0005_remove_rental_duration_days_remove_rental_total_cost_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='Активна'),
        ),
    ]
