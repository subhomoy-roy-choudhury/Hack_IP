from enum import Enum

BASE_WEB_URL = "http://localhost:3000"
GENERATED_REPORT_FOLDER_NAME = "report"
ASSISTANT_NAME = "HackIP Assistant"
ASSISTANT_MODEL = "gpt-3.5-turbo-16k"


class CREDENTIALS_KEYS(Enum):
    # Value format : (<key_name>, <title name of key>)
    OPENAI_API_KEY = ("openai_key", "OpenAI API Key")
    CUTTLY_API_KEY = ("cuttly_key", "Cuttly API Key")
