# Generated by Django 3.0.7 on 2021-04-14 18:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0012_auto_20210412_1749'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topshot',
            name='pic',
            field=models.CharField(max_length=300),
        ),
    ]
