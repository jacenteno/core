# Generated by Django 4.2.5 on 2023-10-26 19:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('lottoluck', '0031_remove_vtasdetalle_iii_premio_relacionado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vtasdetalle',
            name='id_cliente',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='lottoluck.clientes'),
            preserve_default=False,
        ),
    ]
