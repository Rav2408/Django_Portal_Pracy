# Generated by Django 4.0.4 on 2022-05-30 12:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Offers', '0012_alter_application_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='remote',
            field=models.BooleanField(default=False),
        ),
    ]
