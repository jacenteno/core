# Generated by Django 4.2.5 on 2023-10-26 01:31

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    dependencies = [
        ('lottoluck', '0029_numerosorteados_iii_premio_relacionado_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='numerosorteados',
            name='III_premio_relacionado',
        ),
        migrations.RemoveField(
            model_name='numerosorteados',
            name='II_premio_relacionado',
        ),
        migrations.RemoveField(
            model_name='numerosorteados',
            name='I_premio_relacionado',
        ),
        migrations.AddField(
            model_name='vtasdetalle',
            name='III_premio_relacionado',
            field=models.ForeignKey(limit_choices_to={'III_premio__endswith': django.db.models.expressions.CombinedExpression(models.F('III_premio'), '%%', models.Value(100))}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vtasdetalles_III_premio_relacionados', to='lottoluck.numerosorteados'),
        ),
        migrations.AddField(
            model_name='vtasdetalle',
            name='II_premio_relacionado',
            field=models.ForeignKey(limit_choices_to={'II_premio__endswith': django.db.models.expressions.CombinedExpression(models.F('II_premio'), '%%', models.Value(100))}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vtasdetalles_II_premio_relacionados', to='lottoluck.numerosorteados'),
        ),
        migrations.AddField(
            model_name='vtasdetalle',
            name='I_premio_relacionado',
            field=models.ForeignKey(limit_choices_to={'i_premio__endswith': django.db.models.expressions.CombinedExpression(models.F('I_premio'), '%%', models.Value(100))}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='vtasdetalles_i_premio_relacionados', to='lottoluck.numerosorteados'),
        ),
    ]
