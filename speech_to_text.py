import speech_recognition as sr
from typing import Optional

# Инициализация распознавателя речи
speech_recognizer = sr.Recognizer()


def record_text() -> Optional[str]:
    """
    Записывает аудио с микрофона и преобразует его в текст
    Возвращает распознанный текст или None, если запись не удалась
    """
    while True:
        try:
            with sr.Microphone() as source:
                speech_recognizer.adjust_for_ambient_noise(source, duration=0.2)
                print('Слушаю и записываю...')
                audio = speech_recognizer.listen(source)
                print('Запись завершена')
                text = speech_recognizer.recognize_google(audio, language="ru-RU")
                print(f'Вы сказали: {text}')
                return text

        except sr.RequestError as e:
            print(f'Could not request results; {e}')

        except sr.UnknownValueError:
            print('Речь не распознана')
