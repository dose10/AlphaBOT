# -*- coding: utf-8 -*-
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from telegram import Chat
from requests import post, get
from bs4 import BeautifulSoup
import logging
import random as r
import time
import serial
from math import sqrt, gcd
from itertools import count, islice
#from datetime import datetime, date, time, timezone

#a linha abaixo é a utilizada para o token do BOT. por colocar no Github irei comentá-la
#token = gere o seu token
db_path = "http://dontpad.com/alphabot"
#ser = serial.Serial('/dev/ttyUSB0', 9600)
arduino=serial.Serial('COM3', 9600)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)
updater = Updater(token)
memes = []
nomesc = []
phdata = []

# Functions noncommand
def noncommand(bot, update):
    text = (update.message.text).lower()
    ret = ""
    if "sei la" in text:
        ret = "treze"
    elif "porra" in text and "caralho" in text:
        ret = "Ambiente Familiar"
    elif "salve pro gasperini" in text:
        ret = "Lenda que ajudou no começo do BOT!"
    elif "cara" == text.split()[0]:
        carinhas = ["'-'", "'.'", "XD", "u.u", "@.@", ".-.", ":c"]
        ret = r.choice(carinhas)
    elif "boa noite" in text:
        ret = "Boa noite pra quem?"
    elif "bom dia" in text:
        ret = "Bom dia pra quem?" 
    elif "feliz quem" in text:
        ret = "Você diz isso com base em que?"
    elif "boa noite" in text:
        ret = "Já vai tarde..."
    elif "melhor da vida" in text:
        quotes = [
            "pao de alho",
            "acordar cedo e lembrar que é sábado",
            "borda recheada de brinde",
            "quando chega o que vc comprou pela internet",
            "frete grátis",
            "achar dinheiro no bolso",
            "wifi grátis",
            "final da nacional",
        ]
        ret = r.choice(quotes)
    
    if ret:
        update.message.reply_text(ret)


# Functions commanded
def start(bot, update):
    chat_id = update.message.chat_id
    text = "AlphaBOT acordado! Agora você já pode utilizar alguns de meus comando. Tente por /help"
    bot.sendMessage(chat_id=chat_id, text=text)


def help(bot, update):
    chat_id = update.message.chat_id
    text = (
        "Tenho as seguintes funcionalidades\n"
        + "/start - Me acorda caso esteja dormindo\n"
        + "/meme - Frases icônicas de pessoas mais ainda\n"
        + "/add_meme meme - Adicionar um meme\n"
        + "/roll n t - Rola n dados de t faces\n"
        + "/even_odd - O famoso par ou impar\n"
        + "/primo n - Verifica se n é primo\n"
        + "/mute - Apenas admins, muta o Machado\n"
        + "/unmute - Deixa o garoto falar merda vai..."
    )
    bot.sendMessage(chat_id=chat_id, text=text)


def on(bot, update):
    update.message.reply_text("To de pé rs")


def greet(bot, update):
    pre = ["E ai ", "Opa ", "Olá ", "Oie ", "Turu bom "]
    suf = ["pro URI", "pro RU", "pro codeforces", "pro code", "pra maratona"]
    chat_id = update.message.chat_id
    for new_user_obj in update.message.new_chat_members:
        text = "{} {}, bem vindo ao BRUTE. Eu o Bigodera, o bot desssa galera. Bora {}!".format(
            r.choice(pre), new_user_obj["first_name"], r.choice(suf)
        )
        bot.send_message(chat_id=chat_id, text=text)


def meme(bot, update):
    global memes
    text = r.choice(tuple(memes))
    update.message.reply_text(text)

def liga(bot, update): #FUNCOES LIGA E DESLIGA AQUI
    #file1 = open("phisicdata.txt","w")#write mode 
    #file1.write("1") 
    #file1.close()
    #update.message.reply_text("Ligando")
    arduino.write(b'1')
    print("Ligando LED")
    update.message.reply_text("Ligando")

def desliga(bot, update):
    arduino.write(b'0')
    print("Desligando LED")
    update.message.reply_text("Desligando")

"""
def roll(bot, update):
    text = update.message.text.split()
    if len(text) > 1:
        times, limit = map(int, text[1:])
        if times < 100:
            text = "Rolando!\n\n"
            for dice in range(1, times + 1):
                text += str(r.randint(1, limit)) + "\n"
        else:
            text = "Vsf! Porrada de dado"
    else:
        text = str(r.randint(1, 6)) + "\n"
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=text)
"""

"""
def even_odd(bot, update):
    if r.randrange(2):
        text = "Impar"
    else:
        text = "Par"
    chat_id = update.message.chat_id
    bot.send_message(chat_id=chat_id, text=text)
"""

"""
def primo(bot, update):
    def isPrime(n):
        if n < 2:
            return False
        for number in islice(count(2), int(sqrt(n) - 1)):
            if n % number == 0:
                return False
        return True

    def coPrime(a, b):
        return gcd(a, b) == 1

    numbers = list(map(int, update.message.text.split()[1:]))
    if len(numbers) == 1:
        if numbers[0] > 10:
            text = "Sim" if isPrime(numbers[0]) else "Não"
        else:
            update.message.reply_text("Ta de sacanagem né?")
    elif len(numbers) == 2:
        text = ""
        for n in numbers:
            if isPrime(n):
                text += str(n) + " é primo\n"
            else:
                text += str(n) + " não é primo\n"
        if coPrime(numbers[0], numbers[1]):
            text += "São coprimos"
        else:
            text += "Não são coprimos"
    else:
        text = "Mano, para de querer zoar"
    update.message.reply_text(text)
"""

"""
def mute(bot, update):
    chat_id = update.message.chat_id
    admins = [
        str(admin.user.username) for admin in bot.get_chat_administrators(chat_id)
    ]
    user = update.message.from_user.username
    who = update.message.text.split()[1]
    if who == "machado":
        ID = "705600029"
    elif who == "jaasiel":
        ID = "706290557"
    else:
        ID = update.message.from_user.id
    if user in admins:
        bot.restrict_chat_member(chat_id, ID, can_send_messages=False)
        bot.send_message(chat_id=chat_id, text="Cala a boca "+who.capitalize())
    else:
        update.message.reply_text(
            "... cala boca tu"
        )
"""

"""
def unmute(bot, update):
    chat_id = update.message.chat_id
    admins = [
        str(admin.user.username) for admin in bot.get_chat_administrators(chat_id)
    ]
    user = update.message.from_user.username
    who = update.message.text.split()[1]
    if who == "machado":
        ID = "705600029"
    elif who == "jaasiel":
        ID = "706290557"
    if user in admins:
        bot.restrict_chat_member(
            chat_id,
            ID,
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True,
        )
        bot.send_message(chat_id=chat_id, text="Fala gado!")
    else:
        update.message.reply_text("So para admins")

def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)
"""

def main():
    """Start the bot."""
    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Answer in Telegram
    #dp.add_handler(CommandHandler("on", on))
    #dp.add_handler(CommandHandler("start", start))
    #dp.add_handler(CommandHandler("help", help))
    #dp.add_handler(CommandHandler("greet", greet))
    dp.add_handler(CommandHandler("meme", meme))
    dp.add_handler(CommandHandler("liga", liga))
    dp.add_handler(CommandHandler("desliga", desliga))
    #dp.add_handler(CommandHandler("roll", roll))
    #dp.add_handler(CommandHandler("even_odd", even_odd))
    #dp.add_handler(CommandHandler("primo", primo))
    #dp.add_handler(CommandHandler("mute", mute))
    #dp.add_handler(CommandHandler("unmute", unmute))

    # Noncommand answser message on Telegram
    dp.add_handler(MessageHandler(Filters.text, noncommand))

    # log all errors
    #dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


def load_data():
    global memes
    global phdata
    data = pull(db_path)
    memes = data

#def save_data():
#    data = str(contador_caga_pau)+'\n'+'\n'.join(memes)
#    push(db_path, data)
#    push(db_path2, dataNC)

def pull(path):
    data = get(url=path)
    soup = BeautifulSoup(data.text,"html.parser")
    old_text = soup.find('textarea').get_text()
    old_text = old_text.split('\n')

    return old_text

def push(path, text):
    data = {'text':text}

    return post(url=path, data=data)

if __name__ == "__main__":
    load_data()
    main()
