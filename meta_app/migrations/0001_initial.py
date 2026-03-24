from django.db import migrations

class Migration(migrations.Migration):
    operations = [
        migrations.RunSQL(
            sql="CREATE SCHEMA IF NOT EXISTS meta;",
            reverse_sql="DROP SCHEMA meta CASCADE;"
        ),
    ]