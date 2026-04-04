from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from core.models import BaseEntity, BaseDTO
from dataclasses import dataclass
import json


class DicDepartment(MPTTModel, BaseEntity):
    """Структура дерева подразделений"""

    department_parent = TreeForeignKey(
        to="self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="children",
    )

    department_code = models.CharField(
        verbose_name="Код подразделения",  # TODO: Локализация
        max_length=255,
        unique=True,
    )
    department_name = models.CharField(
        verbose_name="Наименование подразделения",  # TODO: Локализация
        max_length=255,
    )
    department_description = models.TextField(
        verbose_name="Детальное описание подразделения",  # TODO: Локализация
    )

    class Meta:
        db_table = '"user_app"."dic_department"'

    class MPTTMeta:
        parent_attr = 'department_parent' # поле родитель


@dataclass
class DicDepartmentDTO(BaseDTO):
    department_code: str
    department_name: str
    department_description: str
    __params__: json = None

    department_parent: DicDepartment = None
