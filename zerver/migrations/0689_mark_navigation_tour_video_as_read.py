# Generated by Django 5.0.9 on 2024-10-21 15:55

from django.db import connection, migrations
from django.db.backends.base.schema import BaseDatabaseSchemaEditor
from django.db.migrations.state import StateApps
from django.utils.timezone import now as timezone_now
from psycopg2.sql import SQL


def mark_navigation_tour_video_as_read(
    apps: StateApps, schema_editor: BaseDatabaseSchemaEditor
) -> None:
    with connection.cursor() as cursor:
        cursor.execute(SQL("SELECT MAX(id) FROM zerver_userprofile;"))
        (max_id,) = cursor.fetchone()

    if max_id is None:
        return

    BATCH_SIZE = 10000
    max_id += BATCH_SIZE / 2
    lower_id_bound = 0
    timestamp_value = timezone_now()
    while lower_id_bound < max_id:
        upper_id_bound = min(lower_id_bound + BATCH_SIZE, max_id)
        with connection.cursor() as cursor:
            query = SQL("""
                INSERT INTO zerver_onboardingstep (user_id, onboarding_step, timestamp)
                SELECT id, 'navigation_tour_video', %(timestamp_value)s
                FROM zerver_userprofile
                WHERE is_bot = False
                AND is_mirror_dummy = False
                AND id > %(lower_id_bound)s AND id <= %(upper_id_bound)s;
                """)
            cursor.execute(
                query,
                {
                    "timestamp_value": timestamp_value,
                    "lower_id_bound": lower_id_bound,
                    "upper_id_bound": upper_id_bound,
                },
            )

        print(f"Processed {upper_id_bound} / {max_id}")
        lower_id_bound += BATCH_SIZE


def mark_navigation_tour_video_as_unread(
    apps: StateApps, schema_editor: BaseDatabaseSchemaEditor
) -> None:
    OnboardingStep = apps.get_model("zerver", "OnboardingStep")

    OnboardingStep.objects.filter(onboarding_step="navigation_tour_video").delete()


class Migration(migrations.Migration):
    atomic = False
    dependencies = [
        ("zerver", "0688_alter_realm_can_resolve_topics_group"),
    ]

    operations = [
        migrations.RunPython(
            mark_navigation_tour_video_as_read,
            reverse_code=mark_navigation_tour_video_as_unread,
            elidable=True,
        ),
    ]
