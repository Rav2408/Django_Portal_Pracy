# Generated by Django 4.0.4 on 2022-05-18 20:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Offers', '0004_alter_company_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='company',
            name='username',
        ),
    ]