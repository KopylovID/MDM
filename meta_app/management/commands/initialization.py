from django.core.management.base import BaseCommand
import subprocess
import sys

class Command(BaseCommand):
    """Команда инициализации"""

    name = 'initialization'
    help = "Инициализация приложения"

    def handle(self, *args, **options):
        self.stdout.write("Запуск инициализации")

        try:
            self.stdout.write(self.style.SUCCESS("\npython manage.py makemigrations user_app"))
            subprocess.run(['python', 'manage.py', 'makemigrations', 'user_app'], text=True, check=True, stdout=self.stdout, stderr=self.stderr)

            self.stdout.write(self.style.SUCCESS("\n\npython manage.py migrate auth"))
            subprocess.run(['python', 'manage.py', 'migrate', 'auth'], text=True, check=True, stdout=self.stdout, stderr=self.stderr)

            self.stdout.write(self.style.SUCCESS("\n\npython manage.py migrate user_app"))
            subprocess.run(['python', 'manage.py', 'migrate', 'user_app'], text=True, check=True, stdout=self.stdout, stderr=self.stderr)

            self.stdout.write(self.style.SUCCESS("\n\npython manage.py migrate"))
            subprocess.run(['python', 'manage.py', 'migrate'], text=True, check=True, stdout=self.stdout, stderr=self.stderr)

            self.stdout.write(self.style.SUCCESS("\n\npython manage.py makemigrations meta_app"))
            subprocess.run(['python', 'manage.py', 'makemigrations', 'meta_app'], text=True, check=True, stdout=self.stdout, stderr=self.stderr)

            self.stdout.write(self.style.SUCCESS("\n\npython manage.py migrate meta_app"))
            subprocess.run(['python', 'manage.py', 'migrate', 'meta_app'], text=True, check=True, stdout=self.stdout, stderr=self.stderr)

            self.stdout.write(self.style.SUCCESS("\n\npython manage.py makemigrations dynamic_tables_app"))
            subprocess.run(['python', 'manage.py', 'makemigrations', 'dynamic_tables_app'], text=True, check=True, stdout=self.stdout, stderr=self.stderr)

            self.stdout.write(self.style.SUCCESS("\n\npython manage.py migrate dynamic_tables_app"))
            subprocess.run(['python', 'manage.py', 'migrate', 'dynamic_tables_app'], text=True, check=True, stdout=self.stdout, stderr=self.stderr)
        except subprocess.CalledProcessError:
            self.stdout.write("Инициализация завершилась с ошибкой")
            sys.exit(1)

        self.stdout.write("\nЗавершение инициализации")
