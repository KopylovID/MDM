from django.core.management.base import BaseCommand
from user_app.models import DicDepartment, DicDepartmentDTO
from typing import Dict


class Command(BaseCommand):
    """Команда наполнения моделей user_app основными данными"""

    name = "user_app_init"
    help = "Инициализирует дерево подразделений"

    def handle(self, *args, **options):
        self.stdout.write("Запуск генерации основных данных - user_app")

        self.stdout.write("Генерация - DicDepartment")
        from .data import DicDepartmentData

        department_dict: Dict[str, DicDepartment] = dict()

        for elem in DicDepartmentData:
            dep_raw = DicDepartmentDTO(*(DicDepartment, *elem))

            dep_parent_code = dict(dep_raw.__params__).get("parent_code")
            if dep_parent_code:
                dep_raw.department_parent = department_dict.get(dep_parent_code)

            dep, created = DicDepartment.objects.update_or_create(
                **dep_raw.get_fields("unique"),
                defaults=dep_raw.get_fields("non-unique"),
            )
            department_dict[dep.department_code] = dep

            if not created:
                dep.save()

        self.stdout.write("Окончание генерации основных данных - user_app")
