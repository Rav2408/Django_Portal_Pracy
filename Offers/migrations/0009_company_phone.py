# Generated by Django 4.0.4 on 2022-05-22 13:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Offers', '0008_alter_offer_company'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='phone',
            field=models.CharField(default=123456789, max_length=20, verbose_name='phone'),
            preserve_default=False,
        ),
    ]
