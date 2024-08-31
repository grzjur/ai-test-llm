import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    MODELS = [
        {'stable': 'ollama', 'model': 'SpeakLeash/bielik-11b-v2.2-instruct-imatrix:Q6_K'},
        {'stable': 'ollama', 'model': 'aya'},
        {'stable': 'ollama', 'model': 'llama3.1'},
        {'stable': 'ollama', 'model': 'qwen2'},
        {'stable': 'ollama', 'model': 'phi3.5'},
        {'stable': 'ollama', 'model': 'mistral'},
        {'stable': 'ollama', 'model': 'mistral-nemo'},
        {'stable': 'anthropic', 'model': 'claude-3-5-sonnet-20240620'},
        {'stable': 'groq', 'model': 'mixtral-8x7b-32768'},
        {'stable': 'groq', 'model': 'gemma2-9b-it'},
        {'stable': 'groq', 'model': 'llama3-8b-8192'},
        {'stable': 'openai', 'model': 'gpt-4o-mini'},
        {'stable': 'openai', 'model': 'gpt-4o'},

    ]


    NUMBER_OF_REPETITIONS = 5

    # API keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY")
    LOCAL_MODEL_PATH = os.getenv("LOCAL_MODEL_PATH")

    SUPERVISOR_STABLE = "openai"
    SUPERVISOR_MODEL = "gpt-4o-mini"

    # Path to questions
    DATA_PATH = "data"
    DATA_FILE = "questions.json"
