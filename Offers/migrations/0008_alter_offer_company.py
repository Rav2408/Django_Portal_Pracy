# Generated by Django 4.0.4 on 2022-05-18 21:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('Offers', '0007_alter_offer_company'),
    ]

    operations = [
        migrations.AlterField(
            model_name='offer',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='Offers.company'),
        ),
    ]
