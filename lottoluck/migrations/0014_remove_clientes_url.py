# Generated by Django 4.2.5 on 2023-09-28 22:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lottoluck', '0013_alter_clientes_tipocliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientes',
            name='url',
        ),
    ]
