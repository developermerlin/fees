# Generated by Django 5.1 on 2024-10-20 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_cs_fees2'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cs_fees2',
            name='cost_of_program',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cs_fees2_cost_of_program_payments', to='app.cs_cost2'),
        ),
    ]
