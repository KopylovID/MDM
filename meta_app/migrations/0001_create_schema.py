from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(sql="CREATE SCHEMA IF NOT EXISTS meta_app;", reverse_sql="DROP SCHEMA meta_app CASCADE;"),
    ]
