from g4f.client import Client
from enum import Enum
import logging
import random

# Инициализация клиента и логгера
client = Client()
logger = logging.getLogger("AI_Request")
logger.setLevel(logging.DEBUG)

# Модели ИИ
class G4FModels(Enum):
    GPT4 = "gpt-4"
    LLAMA3_1 = "llama-3.1-70b"

# Словарь для хранения истории диалогов
conversation_history = {}

# Функция для обрезки истории
def trim_history(history, max_length=4096):
    current_length = sum(len(message["content"]) for message in history)
    while history and current_length > max_length:
        removed_message = history.pop(0)
        current_length -= len(removed_message["content"])
    return history

# Функция для генерации ответа
def generate_response(prompt: str, user_id: int, system_prompt: str = "", max_attempts: int = 5):
    models = list(G4FModels)
    for attempt in range(max_attempts):
        model = random.choice(models)
        try:
            logger.info(f"Попытка {attempt + 1}: Используем модель {model.value}")

            # Добавляем системный промпт, если он есть
            messages = [{"role": "system", "content": system_prompt}] if system_prompt else []
            # Добавляем историю диалога
            messages.extend(conversation_history.get(user_id, []))
            # Добавляем текущий запрос пользователя
            messages.append({"role": "user", "content": prompt})

            # Генерация ответа
            response = client.chat.completions.create(
                model=model.value,
                messages=messages
            )
            content = response.choices[0].message.content

            # Если ответ содержит код, обрамляем его в теги pre и code
            if "```" in content or any(keyword in content for keyword in ['def', 'class']):
                content = f"<pre><code>{content}</code></pre>"

            logger.info(f"Ответ от модели {model.value}: {content}")

            # Обновляем историю диалога
            if user_id not in conversation_history:
                conversation_history[user_id] = []
            conversation_history[user_id].append({"role": "user", "content": prompt})
            conversation_history[user_id].append({"role": "assistant", "content": content})
            conversation_history[user_id] = trim_history(conversation_history[user_id])

            return content
        except Exception as e:
            logger.error(f"Ошибка в попытке {attempt + 1}: {e}")
    return "Не удалось сгенерировать текст."

# Основной цикл чата
if __name__ == '__main__':
    #logging.basicConfig(level=logging.INFO)
    user_id = 1  # Фиктивный ID пользователя для примера
    system_prompt = "Отвечай только на русском!"

    print("Чат с ИИ. Введите 'выход' для завершения.")
    while True:
        prompt = input("Вы: ")
        if prompt.lower() == "выход":
            print("Чат завершён.")
            break

        response = generate_response(prompt, user_id, system_prompt)
        print(f"ИИ: {response}")
