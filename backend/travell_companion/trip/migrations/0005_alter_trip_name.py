# Generated by Django 3.2.12 on 2022-03-05 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0004_alter_tripcompanion_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='name',
            field=models.CharField(max_length=50),
        ),
    ]
