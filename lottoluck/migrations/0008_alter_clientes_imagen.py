# Generated by Django 4.2.5 on 2023-09-27 22:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottoluck', '0007_alter_clientes_imagen'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientes',
            name='imagen',
            field=models.ImageField(blank=True, null=True, upload_to='avatars/'),
        ),
    ]
