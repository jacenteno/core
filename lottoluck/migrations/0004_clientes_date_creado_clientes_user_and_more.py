# Generated by Django 4.2.5 on 2023-09-27 17:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('lottoluck', '0003_alter_clientes_url'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientes',
            name='date_creado',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='clientes',
            name='user',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='vtassorteo',
            name='transaction_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
