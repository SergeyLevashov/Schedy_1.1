import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Области доступа для Google Calendar API
SCOPES = ["https://www.googleapis.com/auth/calendar"]


def authenticate_google_calendar(credentials_path: str, token_path: str) -> Credentials:
    """
    Аутентифицирует пользователя в Google Calendar API
    Возвращает объект Credentials для доступа к API
    """
    creds = None

    # Проверяем, есть ли уже сохраненные учетные данные, чтобы избежать повторной авторизации
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    # Если учетные данные отсутствуют или недействительны, запрашиваем авторизацию
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # Запускаем авторизацию через OAuth, если сохраненных данных нет
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server(port=0)

        # Сохраняем учетные данные в файл для использования в будущем
        with open(token_path, "w") as token:
            token.write(creds.to_json())

    return creds
