import datetime

from pydantic import (
    BaseModel,
    ConfigDict,
)

from backend.core.utilities.formatters.datetime_formatter import format_datetime_into_isoformat
from backend.core.utilities.formatters.field_formatter import format_dict_key_to_camel_case


class BaseSchemaModel(BaseModel):
    """
    Базовая модель Pydantic для схем с общими настройками.

    Особенности:
    - Позволяет создавать модель из атрибутов объектов (from_attributes=True).
    - Валидация данных при присвоении значений (validate_assignment=True).
    - Автоматическое заполнение полей по алиасам (populate_by_name=True).
    - Кастомное кодирование datetime в ISO формат при сериализации в JSON.
    - Генерация алиасов в camelCase из snake_case (alias_generator).

    Используется как базовый класс для всех схем данных в проекте.
    """

    model_config = ConfigDict(
        from_attributes=True,
        validate_assignment=True,
        populate_by_name=True,
        json_encoders={
            datetime.datetime: format_datetime_into_isoformat
        },
        alias_generator=format_dict_key_to_camel_case,
    )
