import json
import asyncio
from datetime import datetime
from speech_to_text import record_text
from event_processing import process_text
from add_calendar_event import add_event_to_calendar
from google_auth import authenticate_google_calendar

# Константы для путей к файлам и временной зоны
CREDENTIALS_PATH = "config/credentials.json"
TOKEN_PATH = "config/token.json"
TIME_ZONE = "Asia/Yekaterinburg"


def print_event_data(event):
    """
    Выводит данные события в формате JSON для проверки перед добавлением в календарь
    """
    print("\nДанные для добавления в календарь:")
    print(json.dumps(event, indent=4, ensure_ascii=False))


def create_event_dict(event_data):
    """
    Форматирует данные о событии в структуру, подходящую для Google Calendar API
    """
    return {
        'summary': event_data.title,
        'location': event_data.location or '',
        'description': event_data.description or '',
        'start': {
            'dateTime': event_data.start_time.isoformat(),
            'timeZone': TIME_ZONE,
        },
        'end': {
            'dateTime': event_data.end_time.isoformat() if event_data.end_time else event_data.start_time.isoformat(),
            'timeZone': TIME_ZONE,
        },
        'recurrence': [f"RRULE:FREQ={event_data.repeat_frequency.upper()}"] if event_data.repeat_frequency != "none"
        else [],
        "attendees": [],  # Участники (пока не используются)
    }


async def main():
    """
    Основная функция для записи речи, обработки текста и добавления события в календарь
    """
    # Записываем речь с микрофона и преобразуем её в текст
    user_input = record_text()

    # Если текст не был распознан, завершаем выполнение
    if not user_input:
        print("Не удалось записать текст. Программа завершена.")
        return

    # Текущая дата для обработки текста (например, для событий "сегодня")
    current_date = datetime.now().strftime("%Y-%m-%d")

    # Извлекаем данные о событии из текста.
    event_data = await process_text(user_input, current_date)

    # Если данные о событии не удалось извлечь, завершаем выполнение
    if not event_data:
        print("Не удалось извлечь данные о событии. Программа завершена.")
        return

    # Формируем словарь для Google Calendar
    event = create_event_dict(event_data)

    # Аутентификация пользователя и добавление события в календарь
    creds = authenticate_google_calendar("config/credentials.json", "config/token.json")
    add_event_to_calendar(event, creds)


if __name__ == '__main__':
    asyncio.run(main())
