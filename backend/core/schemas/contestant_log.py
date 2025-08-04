from dataclasses import dataclass

from backend.core.schemas.base import BaseSchemaModel


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
