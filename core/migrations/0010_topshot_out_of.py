# Generated by Django 3.0.7 on 2021-04-05 19:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_set_img_link'),
    ]

    operations = [
        migrations.AddField(
            model_name='topshot',
            name='out_of',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
