# Generated by Django 2.0.7 on 2018-07-09 18:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jarvis', '0002_auto_20180709_1515'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itenslista',
            options={'verbose_name': 'item da lista', 'verbose_name_plural': 'itens da lista'},
        ),
        migrations.AddField(
            model_name='itenslista',
            name='categoria',
            field=models.CharField(default='', max_length=10),
        ),
    ]
