import telebot
import config
from telebot import types


bot = telebot.TeleBot(config.TOKEN)

user_dict = {}


class User:
    def __init__(self, city):
        self.city = city

        keys = ['name', 'secondname', 'phone', 'email']

        for key in keys:
            self.key = None


@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    itembtn1 = types.KeyboardButton('/about')
    itembtn2 = types.KeyboardButton('/registration')
    itembtn3 = types.KeyboardButton('/help')
    itembtn4 = types.KeyboardButton('/site')
    markup.add(itembtn1, itembtn2,itembtn3, itembtn4)

    mess = f'Здравствуйте, <b>{message.from_user.first_name} {message.from_user.last_name}</b>'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(commands=['registration'])
def user_reg(message):
    msg = bot.send_message(message.chat.id, 'Ваш город?')
    bot.register_next_step_handler(msg, process_city_step)


def process_city_step(message):
    try:
        chat_id = message.chat.id
        user_dict[chat_id] = User(message.text)

        msg = bot.send_message(chat_id, 'Ваше имя?')
        bot.register_next_step_handler(msg,process_name_step)

    except Exception as e:
        bot.reply_to(message, 'Упс, не указан Ваш город')


def process_name_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.name = message.text

        msg = bot.send_message(chat_id, 'Ваша фамилия?')
        bot.register_next_step_handler(msg, process_secondname_step)

    except Exception as e:
        bot.reply_to(message, 'Упс, нет Вашего имени')


def process_secondname_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.secondname = message.text

        msg = bot.send_message(chat_id, 'Ваш номер телефона?')
        bot.register_next_step_handler(msg, process_phone_step)

    except Exception as e:
        bot.reply_to(message, 'Упс, нет Вашей фамилии')


def process_phone_step(message):
    try:
        int(message.text)

        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.phone = message.text

        msg = bot.send_message(chat_id, 'Ваш Email?')
        bot.register_next_step_handler(msg, process_email_step)

    except Exception as e:
        msg = bot.reply_to(message, 'Упс, введите верный номер телефона')
        bot.register_next_step_handler(msg, process_phone_step)


def process_email_step(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        user.email = message.text

        mess = f'Заявка: {user.city} {user.name} {user.secondname} {user.phone} {user.email}'
        bot.send_message(chat_id, mess, parse_mode='html')
        bot.send_message(config.CHAT_ID, mess, parse_mode='html')

    except Exception as e:
        bot.reply_to(message, 'Упс...')


@bot.message_handler(commands=['site'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("Перейти на сайт", url=config.SITE))
    bot.send_message(message.chat.id, config.COMPANY_NAME, reply_markup=markup)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, config.HELP, parse_mode='html')


@bot.message_handler(commands=['about'])
def about(message):
    bot.send_message(message.chat.id, config.ABOUT, parse_mode='html')

#проверить свой ID
@bot.message_handler(content_types=['text'])
def get_user_text(message):
    if message.text == "ID":
        bot.send_message(message.chat.id, f"ID {message.from_user.id}", parse_mode='html')


bot.polling(none_stop=True)
