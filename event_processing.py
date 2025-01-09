import json
from datetime import datetime
from typing import Optional, List
import dateparser
from ollama import AsyncClient
from pydantic import BaseModel, ValidationError


class EventData(BaseModel):
    """
    Модель данных для события, используемая для валидации и хранения информации
    """
    title: str
    location: Optional[str] = None
    description: Optional[str] = None
    start_time: datetime
    end_time: Optional[datetime] = None
    repeat_frequency: Optional[str] = None
    recurrence: Optional[List[str]] = None
    attendees: Optional[List[str]] = None
    timeZone: Optional[str] = "UTC"


def get_rrule(frequency: str, count: Optional[int] = None) -> Optional[str]:
    """
    Преобразует частоту повторения события в строку RRULE
    """
    frequency_map = {
        "none": None,
        "daily": "RRULE:FREQ=DAILY",
        "weekly": "RRULE:FREQ=WEEKLY",
        "monthly": "RRULE:FREQ=MONTHLY",
        "yearly": "RRULE:FREQ=YEARLY",
    }

    if frequency not in frequency_map:
        return None

    base_rule = frequency_map[frequency]
    return f"{base_rule};COUNT={count}" if count else base_rule


def correct_date_format(date_str: str) -> str:
    """
    Корректирует формат даты, если он неправильный (например, YYYY-DD-MM -> YYYY-MM-DD)
    """
    parsed_date = dateparser.parse(date_str, languages=["ru"])

    return parsed_date.isoformat() if parsed_date else date_str


def generate_prompt(text: str, current_date: str) -> str:
    """
    Генерирует промпт для модели
    """
    return f"""
        Извлеки из текста информацию о событии и верни её в формате JSON. Следуй следующим правилам:
        1. Название события должно быть кратким и отражать суть события.
        2. Укажи место, если оно есть в тексте.
        3. Укажи описание, если оно есть в тексте.
        4. Укажи время начала события в формате ISO 8601 (YYYY-MM-DDTHH:MM:SS).
            - Если в тексте указано "сегодня", используй текущую дату: {current_date}.
            - Если в тексте указано "завтра", используй завтрашнюю дату.
            - Если в тексте указан день недели (например, "следующий понедельник"), вычисли дату.
        5. Укажи время окончания события в формате ISO 8601, если оно есть в тексте.
        6. Укажи частоту повторения события (none, daily, weekly, monthly, yearly), если она есть в тексте.

        Пример 1:
        Текст: "Запланируй ежемесячную встречу с бухгалтерией 15 числа в 12:00"
        JSON:
        {{
          "title": "Встреча с бухгалтерией",
          "location": null,
          "description": null,
          "start_time": "2025-01-15T12:00:00",
          "end_time": null,
          "repeat_frequency": "monthly"
        }}

        Текст: {text}

        Твоя задача: ответить только JSON, без каких-либо объяснений, комментариев или кода. Любой текст вне JSON строго
        запрещён!
        """


async def process_text(text: str, current_date: str) -> Optional[EventData]:
    """
    Извлекает данные о событии из текста с помощью модели и возвращает их в структурированном виде
    """
    response = None
    try:
        # Инициализация клиента для взаимодействия с моделью Ollama
        client = AsyncClient()
        prompt = generate_prompt(text, current_date)

        # Запрос к модели для извлечения данных о событии
        response = await client.chat(
            model='llama3.2-vision',
            messages=[{'role': 'user', 'content': prompt}],
            options={'temperature': 0},  # Делаем ответы более детерминированными
        )

        # Парсинг JSON из ответа модели
        json_data = json.loads(response['message']['content'])

        # Настройки для корректного парсинга дат
        settings = {
            "DATE_ORDER": "YMD",
            "PREFER_DATES_FROM": "future",
        }

        if "start_time" in json_data:
            parsed_start = dateparser.parse(json_data["start_time"], languages=["ru"], settings=settings)
            if parsed_start:
                json_data["start_time"] = parsed_start.strftime("%Y-%m-%dT%H:%M:%S")

        if "end_time" in json_data and json_data["end_time"]:
            parsed_end = dateparser.parse(json_data["end_time"], languages=["ru"], settings=settings)
            if parsed_end:
                json_data["end_time"] = parsed_end.strftime("%Y-%m-%dT%H:%M:%S")

        # Валидация данных с помощью Pydantic
        event_data = EventData.model_validate(json_data)

        # Удаление информации о временной зоне
        event_data.start_time = event_data.start_time.replace(tzinfo=None)
        if event_data.end_time:
            event_data.end_time = event_data.end_time.replace(tzinfo=None)

        return event_data

    except ValidationError as e:
        print(f"\nОшибка валидации при обработке текста: {text}")
        print(f"Ошибка: {str(e)}")
        print("-" * 50)

    except Exception as e:
        print(f"\nОшибка при обработке текста: {text}")
        print(f"Ошибка: {str(e)}")
        print(f"Ответ модели: {response['message']['content'] if 'response' in locals() else 'Не доступен'}")
        print("-" * 50)
