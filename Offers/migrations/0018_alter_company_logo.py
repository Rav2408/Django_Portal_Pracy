# Generated by Django 4.0.4 on 2022-06-05 12:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Offers', '0017_alter_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, default=None, null=True, upload_to='logo/'),
        ),
    ]
