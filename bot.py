import telebot

import models
from config import bot_token, master_uid
models.initialize()
bot = telebot.TeleBot(bot_token)


@bot.message_handler(commands=['start'])
def start(message):
    try:
        models.User.create(uid=message.chat.id)
    except models.IntegrityError:
        bot.send_message(message.chat.id, "You already have a permanent account")
    else:
        bot.send_message(message.chat.id, "Permanent account created =)")


@bot.message_handler(commands=['set_username'])
def set_username(message):
        try:
            username = message.text.split()[1]
        except IndexError:
            bot.send_message(message.chat.id, "It's /set_username <username>")
            return 0
        bot.send_message(message.chat.id, "Changing your username to '{}'...".format(username))
        try:
            models.User.update(username=username).where(models.User.uid == message.chat.id).execute()
        except models.IntegrityError:
            bot.send_message(message.chat.id, "Username is already taken")
        else:
            bot.send_message(message.chat.id, "Your username is now '{}'".format(
                models.User.get(models.User.uid == message.chat.id).username))


@bot.message_handler(commands=['add_music'])
def add_music(message):

    try:
        admin = models.User.get(models.User.uid == message.chat.id).admin
    except models.DoesNotExist:
        bot.send_message(message.chat.id, "You have no permanent account\n/create will get you one!")
        return 1
    try:
        content = message.text.split()[1:]
        content = "".join(content)
    except IndexError:
        bot.send_message(message.chat.id, "It's /add_music <soundcloud_iframe>")
        return 1

    if admin:
        models.EditorPick.create(cat='1',
                                 content=content)
        bot.send_message(message.chat.id, "Added your post!")


@bot.message_handler(commands=['me'])
def me(message):
    try:
        username = models.User.get(models.User.uid == message.chat.id).username
    except models.DoesNotExist:
        bot.send_message(message.chat.id, "You have no permanent account\n/create will get you one!")
    else:
        if username:
            bot.send_message(message.chat.id, "'{}'".format(username))
        else:
            bot.send_message(message.chat.id, "No username was set")


@bot.message_handler(func=lambda m: True)
def send_welcome(message):
    bot.send_message(message.chat.id, "Your login:\n{}".format(message.chat.id))


while True:
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        bot.send_message(master_uid, "Crashed with {}".format(e))
