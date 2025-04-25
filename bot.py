import telebot
import requests
from decouple import config
import psycopg2


# Подключение к базе данных
conn = psycopg2.connect(dbname=config('DBname'), user=config('PUser'), password=config('Password'), host=config('Host'), port=config('Port'))
cursor = conn.cursor()


# Подключение к боту Телеграмма по токену
bot = telebot.TeleBot(config('TokenBot'))

# Подключение к ИИ GigaChat от Сбера
from gigachat import GigaChat

giga = GigaChat(
   credentials=config('Authorization_key'),
   verify_ssl_certs=False
)


# Работа с отправленными сообщениями пользователя в телеграм-боте
@bot.message_handler(content_types=['text'])
def get_text_messages(message):
    cursor.execute("CREATE TABLE IF NOT EXISTS history (id SERIAL PRIMARY KEY, chat_user text, user_text text,answer text)")
    conn.commit()
    if message.text == "/start":
        bot.send_message(message.from_user.id, "Привет! Бот работает!")
    elif message.text == "/help":
        bot.send_message(message.from_user.id, "Введи любое сообщение, и GigaChat тебе ответит!  ;)")
    else:
        # Подключение GigaChat для обработки запроса пользователя в телеграм-боте
        if __name__ == '__main__':
            giga.get_token()
            user_prompt = message.text
            response = giga.chat(user_prompt)
            response_chat = response.choices[0].message.content
            if response_chat:
                bot.send_message(message.from_user.id, response_chat)
                # Занесение запроса в базу данных
                data = (message.from_user.id, message.text, response_chat)
                cursor.execute("INSERT INTO history (chat_user, user_text, answer) VALUES (%s, %s, %s)", data)
                conn.commit()


# Проверка наличия сообщений телеграм-бота
bot.polling(none_stop=True, interval=0)

# Отключение от базы данных
cursor.close()
conn.close()
