from django.core.management.base import BaseCommand
from meta_app.models import (
    DicAttrType,
    DicAttrTypeDTO,
    DicAttrGroup,
    DicAttrGroupDTO,
    DicAttr,
    DicAttrDTO,
)
from dataclasses import asdict
from typing import Dict


class Command(BaseCommand):
    """Команда наполнения моделей основными даными"""

    help = "Генерация основных данных"

    def handle(self, *args, **options):
        self.stdout.write("Запуск генерации основных данных")

        attr_type_dict: Dict[str, DicAttrType] = dict()
        attr_group_dict: Dict[str, DicAttrGroup] = dict()

        self.stdout.write("Генерация - DicAttrType")
        from .data import DicAttrTypeData

        for elem in DicAttrTypeData:
            attr_type_raw = DicAttrTypeDTO(*(DicAttrType, *elem))
            attr_type, created = DicAttrType.objects.update_or_create(
                **attr_type_raw.get_fields('unique'),
                defaults=attr_type_raw.get_fields('non-unique')
            )
            attr_type_dict[attr_type.type_code] = attr_type
            if not created:
                attr_type.save()

        self.stdout.write("Генерация - DicAttrGroup")
        from .data import DicAttrGroupData

        for elem in DicAttrGroupData:
            attr_group_raw = DicAttrGroupDTO(*(DicAttrGroup, *elem))
            attr_group, created = DicAttrGroup.objects.update_or_create(
                **attr_group_raw.get_fields('unique'),
                defaults=attr_group_raw.get_fields('non-unique')
            )
            attr_group_dict[attr_group.group_code] = attr_group
            if not created:
                attr_group.save()

        self.stdout.write("Генерация - DicAttr")
        from .data import DicAttrData

        for elem in DicAttrData:
            attr_raw = DicAttrDTO(*(DicAttr, *elem))
            attr_raw.attr_type = attr_type_dict.get(attr_raw.__attr_type__)
            attr_raw.attr_group = attr_group_dict.get(attr_raw.__attr_group__)
            attr, created = DicAttr.objects.update_or_create(
                **attr_raw.get_fields('unique'),
                defaults=attr_raw.get_fields('non-unique')
            )
            if not created:
                attr.save()

        self.stdout.write("Окончание генерации основных данных")
