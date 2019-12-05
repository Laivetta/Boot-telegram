
import logging

from telegram import *
from telegram.__main__ import main as tmain
from telegram.ext import *

logging.basicConfig(format='%(asctime)-15s %(message)s', level=logging.DEBUG)


def start(bot, update):
    bot.send_message(update.message.chat_id, "Got message")


def main():
    updater = Updater(token='808767729:AAE4gOGYfBxDFOldbnWia34RimXiJWsiQt8')
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))

    updater.start_polling()


if __name__ == '__main__':
    tmain()
    main()
 
