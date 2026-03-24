from django.core.management.base import BaseCommand
from meta_app.models import DicAttrType, DicAttrTypeDTO
from dataclasses import asdict


class Command(BaseCommand):
    """Команда наполнения моделей основными даными"""

    help = 'Генерация основных данных'

    def handle(self, *args, **options):
        self.stdout.write('Запуск генерации основных данных')

        self.stdout.write('Генерация - DicAttrType')
        from .data import DicAttrTypeData
        for elem in DicAttrTypeData:
            attr_raw = DicAttrTypeDTO(*elem)
            attr, created = DicAttrType.objects.get_or_create(**asdict(attr_raw))
            if not created:
                attr.save()
        self.stdout.write('Окончание генерации основных данных')
