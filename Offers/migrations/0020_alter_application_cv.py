# Generated by Django 4.0.4 on 2022-06-07 14:34

import Offers.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Offers', '0019_alter_application_offer'),
    ]

    operations = [
        migrations.AlterField(
            model_name='application',
            name='cv',
            field=models.FileField(default=None, upload_to='uploads/', validators=[Offers.validators.validate_file_extension, Offers.validators.file_size]),
        ),
    ]
