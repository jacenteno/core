# Generated by Django 4.2.5 on 2023-10-17 23:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lottoluck', '0022_alter_vtasdetalle_id_vtasorteo_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='vtassorteo',
            name='pdf_file',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
