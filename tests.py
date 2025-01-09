import asyncio
from datetime import datetime
from main import create_event_dict
from event_processing import process_text
from add_calendar_event import add_event_to_calendar
from google_auth import authenticate_google_calendar


async def test_event_extraction_and_event_creating():

    current_date = datetime.now().strftime("%Y-%m-%d")

    test_strings = [
        "Запланируй встречу с командой разработчиков завтра в 15:00 в переговорной А",
        "Создай ежедневную задачу проверять почту в 10 утра",
        "Назначь созвон с клиентом на следующий вторник в 14:30, длительность 1 час",
        "Установи напоминание о тренировке каждый понедельник в 18:00 в спортзале на Ленина",
        "Добавь встречу сегодня в 16:00"
    ]
    for test_string in test_strings:
        event_data = await process_text(test_string, current_date)

        if not event_data:
            print("Не удалось извлечь данные о событии. Программа завершена.")
            return

        event = create_event_dict(event_data)

        creds = authenticate_google_calendar("config/credentials.json", "config/token.json")
        add_event_to_calendar(event, creds)

    # Выводим информацию о созданном событии для проверки.
    # print(f"\nИсходный текст: {test_string}")
    # print("\nИзвлеченные данные:")
    # print(f"Название: {event_data.title}")
    # print(f"Место: {event_data.location or 'Не указано'}")
    # print(f"Описание: {event_data.description or 'Не указано'}")
    # print(f"Начало: {event_data.start_time}")
    # print(f"Окончание: {event_data.end_time or 'Не указано'}")
    # print(f"Повторение: {event_data.repeat_frequency}")
    # print("-" * 50)


if __name__ == '__main__':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(test_event_extraction_and_event_creating())
