# Generated by Django 3.0.7 on 2021-02-15 19:06

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='topShot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_name', models.CharField(max_length=60)),
                ('team', models.CharField(max_length=100)),
                ('price', models.TextField()),
                ('play_type', models.CharField(max_length=15)),
                ('set_name', models.CharField(max_length=50)),
                ('rarity', models.CharField(max_length=50)),
            ],
        ),
    ]
