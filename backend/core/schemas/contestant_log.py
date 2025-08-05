from dataclasses import dataclass
from datetime import datetime
from typing import Sequence
from pydantic import Field
from backend.core.models.contestant_log import ContestantLogLevelType
from backend.core.schemas.base import BaseSchemaModel
from backend.core.utilities.server import get_server_time


@dataclass
class LogMessage:
    # Сообщение при списании point's со счета
    balance_decrease = lambda points: (
        f"С вашего счета списано {points} очков."
    )
    # Сообщение при начислении point's на счет
    balance_increase = lambda points: (
        f"На ваш счет начислено {points} очков."
    )
    # Добавлена задача
    add_selected_problem = lambda category_name, category_price: (
        f"К вашим активным карточкам добавлена карточка <{category_name} за {category_price}>."
    )
    # Неверный ответ на задачу
    wrong_answer = lambda: (
        "Ответ неверный."
    )
    # Верный ответ на задачу
    correct_answer = lambda: (
        "Ответ засчитан."
    )


class ContestantLogId(BaseSchemaModel):
    contestant_log_id: int


class ContestantLogInfo(BaseSchemaModel):
    contestant_log_id: int
    log_level: ContestantLogLevelType
    content: str
    created_at: datetime


class ContestantLogPaginatedResponse(BaseSchemaModel):
    total: int
    offset: int
    limit: int
    body: Sequence[ContestantLogInfo]
    server_time: datetime = Field(
        default_factory=lambda: get_server_time(with_server_timezone=True)
    )
