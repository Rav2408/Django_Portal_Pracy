# Generated by Django 4.0.4 on 2022-06-03 13:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Offers', '0015_alter_company_logo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='position',
            field=models.CharField(max_length=50, verbose_name='position'),
        ),
    ]
