from django.db import migrations


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.RunSQL(sql="CREATE SCHEMA IF NOT EXISTS user_app;", reverse_sql="DROP SCHEMA user_app CASCADE;"),
    ]
