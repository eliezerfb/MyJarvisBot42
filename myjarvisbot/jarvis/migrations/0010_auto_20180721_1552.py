# Generated by Django 2.0.7 on 2018-07-21 18:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jarvis', '0009_auto_20180716_0831'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itenslista',
            name='secao',
            field=models.PositiveSmallIntegerField(blank=True, choices=[(10, 'Cereais'), (20, 'Mercearia'), (30, 'Frios'), (35, 'Padaria'), (40, 'Hortifruti'), (50, 'Carnes'), (60, 'Higiene'), (70, 'Limpeza'), (80, 'Bebidas'), (90, 'Outros')], default=90, verbose_name='seção'),
        ),
    ]