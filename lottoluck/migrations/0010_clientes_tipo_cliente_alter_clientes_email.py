# Generated by Django 4.2.5 on 2023-09-28 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottoluck', '0009_alter_clientes_imagen'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='tipo_cliente',
            field=models.IntegerField(choices=[[0, 'Regular'], [1, 'Especial'], [2, 'VIP'], [3, 'Compra Credido']], default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='clientes',
            name='email',
            field=models.EmailField(max_length=255, null=True, verbose_name='Correo'),
        ),
    ]
