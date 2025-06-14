# Generated by Django 5.2 on 2025-05-22 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentals', '0007_alter_damage_options_alter_damage_car'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='damage',
            options={'verbose_name': 'Повреждение', 'verbose_name_plural': 'Повреждения'},
        ),
        migrations.AlterField(
            model_name='car',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='car_images/', verbose_name='Добавить фото'),
        ),
        migrations.AlterField(
            model_name='car',
            name='is_available',
            field=models.BooleanField(default=True, verbose_name='Доступен'),
        ),
    ]
