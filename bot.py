import telebot
import requests
from decouple import config


# Подключение к боту Телеграмма по токену
bot = telebot.TeleBot(config('TokenBot'))

# Подключение к ИИ GigaChat от Сбера
TOKEN = config('TokenChat')
URL = 'https://api.gigachat.sber.ru/v1/chat/completions'


def send_request(prompt):
    headers = {
        'Authorization': f'Bearer {TOKEN}',
        'Content-Type': 'application/json',
    }
    data = {
        'model': 'gpt-3.5-turbo',  # Модель GigaChat, может зависеть от конфигурации
        'messages': [
            {'role': 'system', 'content': 'You are a helpful assistant.'},
            {'role': 'user', 'content': prompt}
        ]
    }

    response = requests.post(URL, json=data, headers=headers)

    if response.status_code == 200:
        return response.text
    else:
        print(f'Ошибка: {response.status_code}')
        return None


# Работа с отправленными сообщениями пользователя в телеграм-боте
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Бот работает!")
    if message.text:
        # Подключение GigaChat для обработки запроса пользователя в телеграм-боте
        if __name__ == '__main__':
            user_prompt = message.text
            result = send_request(user_prompt)
            if result:
                answer = result['choices'][0]['message']['content']
                bot.send_message(message.from_user.id, answer)

# Проверка наличия сообщений телеграм-бота
bot.polling(none_stop=True, interval=0)
