from django.core.management.base import BaseCommand
from meta_app.models import (
    AttrType,
    AttrTypeDTO,
    AttrGroup,
    AttrGroupDTO,
    Attr,
    AttrDTO,
    Structure,
    StructureDTO
)
from typing import Dict


class Command(BaseCommand):
    """Команда наполнения моделей meta_app основными данными"""

    name = 'meta_app_init'
    help = "Генерация основных данных"

    def handle(self, *args, **options):
        self.stdout.write("Запуск генерации основных данных - meta_app")

        attr_type_dict: Dict[str, AttrType] = dict()
        attr_group_dict: Dict[str, AttrGroup] = dict()

        self.stdout.write("Генерация - DicAttrType")
        from .data import AttrTypeData

        for elem in AttrTypeData:
            attr_type_raw = AttrTypeDTO(*(AttrType, *elem))
            attr_type, created = AttrType.objects.update_or_create(
                **attr_type_raw.get_fields('unique'),
                defaults=attr_type_raw.get_fields('non-unique')
            )
            attr_type_dict[attr_type.type_code] = attr_type
            if not created:
                attr_type.save()

        self.stdout.write("Генерация - DicAttrGroup")
        from .data import AttrGroupData

        for elem in AttrGroupData:
            attr_group_raw = AttrGroupDTO(*(AttrGroup, *elem))
            attr_group, created = AttrGroup.objects.update_or_create(
                **attr_group_raw.get_fields('unique'),
                defaults=attr_group_raw.get_fields('non-unique')
            )
            attr_group_dict[attr_group.group_code] = attr_group
            if not created:
                attr_group.save()

        self.stdout.write("Генерация - DicAttr")
        from .data import AttrData

        for elem in AttrData:
            attr_raw = AttrDTO(*(Attr, *elem))
            attr_raw.attr_type = attr_type_dict.get(attr_raw.__attr_type__)
            attr_raw.attr_group = attr_group_dict.get(attr_raw.__attr_group__)
            attr, created = Attr.objects.update_or_create(
                **attr_raw.get_fields('unique'),
                defaults=attr_raw.get_fields('non-unique')
            )
            if not created:
                attr.save()

        self.stdout.write("Генерация - Structure")
        from .data import StructureData

        structure_dict: Dict[str, Structure] = dict()

        for elem in StructureData:
            struct_raw = StructureDTO(*(Structure, *elem))

            struct_parent_code = dict(struct_raw.__params__).get("parent_code")
            if struct_parent_code:
                struct_raw.department_parent = structure_dict.get(struct_parent_code)

            struct, created = Structure.objects.update_or_create(
                **struct_raw.get_fields("unique"),
                defaults=struct_raw.get_fields("non-unique"),
            )
            structure_dict[struct.structure_code] = struct

            if not created:
                struct.save()

        self.stdout.write("Окончание генерации основных данных - meta_app")
