# Generated by Django 4.0.4 on 2022-06-02 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Offers', '0013_alter_offer_remote'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='Offers/static/logo'),
        ),
    ]
