# Generated by Django 2.0.7 on 2018-07-15 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jarvis', '0005_userstelegram'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itenslista',
            name='produto',
            field=models.CharField(max_length=50),
        ),
    ]
