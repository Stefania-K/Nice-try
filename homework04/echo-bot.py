import telebot

access_token = '1052904358:AAEAnoNyZjSQqb2lf4OI8T0FHCFGPouXc8c'
telebot.apihelper.proxy = {'https': 'https://51.15.120.43:3128'}

# Создание бота с указанным токеном доступа
bot = telebot.TeleBot(access_token)


@bot.message_handler(content_types=['text'])
def echo(message):
    bot.send_message(message.chat.id, message.text)


if __name__ == '__main__':
    bot.polling()
