# Generated by Django 4.2.5 on 2023-10-26 20:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lottoluck', '0034_vtasdetalle_id_cliente'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vtasdetalle',
            name='id_cliente',
        ),
    ]