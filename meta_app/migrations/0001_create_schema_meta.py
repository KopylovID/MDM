from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(sql="CREATE SCHEMA IF NOT EXISTS meta;", reverse_sql="DROP SCHEMA meta CASCADE;"),
    ]
