from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


def add_event_to_calendar(event_data: dict, creds) -> None:
    """
    Добавляет событие в Google Calendar на основе переданных данных
    """
    try:
        # Создаем сервис Google Calendar для взаимодействия с API
        service = build('calendar', 'v3', credentials=creds)

        # Добавляем событие в календарь пользователя (по умолчанию 'primary')
        event = service.events().insert(calendarId='primary', body=event_data).execute()

        # Выводим ссылку на созданное событие для удобства пользователя
        print(f"Событие создано: {event.get('htmlLink')}")

    except HttpError as e:
        print(f"Ошибка при добавлении события в календарь: {e}")
