# Generated by Django 3.2.12 on 2022-03-07 08:39

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0005_alter_trip_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('city_id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('city_name', models.CharField(max_length=30)),
                ('country', models.CharField(max_length=30)),
                ('population', models.IntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('rating', models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
            options={
                'db_table': 'City',
            },
        ),
        migrations.CreateModel(
            name='TripCity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dest_city_order', models.IntegerField(verbose_name=django.core.validators.MinValueValidator(1))),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip.city')),
                ('trip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trip.trip')),
            ],
            options={
                'db_table': 'TripCity',
            },
        ),
    ]
