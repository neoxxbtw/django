# Generated by Django 5.2 on 2025-05-22 18:30

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0010_alter_rental_duration_days_alter_rental_total_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rental',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rental', to='rentals.car', verbose_name='Автомобиль'),
        ),
    ]
