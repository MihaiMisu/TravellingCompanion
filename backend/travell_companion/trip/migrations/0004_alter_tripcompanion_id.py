# Generated by Django 3.2.12 on 2022-03-05 07:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trip', '0003_alter_tripcompanion_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tripcompanion',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]