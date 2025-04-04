# Generated by Django 5.0.10 on 2025-02-17 09:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("zerver", "0674_set_default_for_stream_can_subscribe_group"),
    ]

    operations = [
        migrations.AlterField(
            model_name="stream",
            name="can_subscribe_group",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.RESTRICT,
                related_name="+",
                to="zerver.usergroup",
            ),
        ),
    ]
