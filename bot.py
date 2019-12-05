#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.

https://descubriendolaorangepi.wordpress.com/2017/02/18/desarrollando-un-bot-de-telegram-en-python-que-permita-consultar-y-controlar-un-sistema-linux-armbian/
 1– Instalamos las herramientas necesarias:

sudo apt-get install python
sudo apt-get install python-pip
sudo apt-get install python-dev
sudo apt-get install python-setuptools
2 – Instalamos la librería:

sudo pip install python-telegram-bot --upgrade


"""


 
# Importar librerias

import logging
import os
import sys
import time
import numbers
import subprocess

# Importar desde librerias
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters, RegexHandler, ConversationHandler, CallbackQueryHandler)
 
##############################


from telegram.ext import Updater, CommandHandler, MessageHandler, Filters


##############################
 
# Funcion para realizar llamadas del sistema (ejecutar comandos Linux)
def llamadaSistema(entrada):
    salida = "" # Creamos variable vacia
    f = os.popen(entrada) # Llamada al sistema
    for i in f.readlines(): # Leemos caracter a caracter sobre la linea devuelta por la llamada al sistema
        salida += i  # Insertamos cada uno de los caracteres en nuestra variable
    salida = salida[:-1] # Truncamos el caracter fin de linea '\n'
 
    return salida # Devolvemos la respuesta al comando ejecutado
 
##############################


# Enable logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)





# Define a few command handlers. These usually take the two arguments bot and
# update. Error handlers also receive the raised TelegramError object in error.
def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update, context):
    """Echo the user message."""
    update.message.reply_text(update.message.text)
    
# Manejador correspondiente al comando /ip
def ip(update, context):
    ip_afuera = llamadaSistema("curl ipinfo.io/ip") # Llamada al sistema
    update.message.reply_text (ip_afuera) # Respondemos al comando con el mensaje    
    

 # Manejador correspondiente al riego
def regar(update, context):
        riego = llamadaSistema("mosquitto_pub -h 192.168.100.200 -t '/entrada/riego' -m 1") # Llamada al sistema    
        update.message.reply_text(riego) # Respondemos al comando con el mensaje

 # Manejador correspondiente a temperatura exterior
def temp(update, context):
        temperatura = llamadaSistema("mosquitto_sub -h 192.168.100.200 -t '/salida/exterior/temperatura/#'") # Llamada al sistema 
        update.message.reply_text(temperatura) # Respondemos al comando con el mensaje


# Manejador correspondiente al comando /apagar
def apagar(update, context):
     update.message.reply_text("Apagando el sistema") # Respondemos al comando con el mensaje
     llamadaSistema("shutdown -h now") # Llamada al sistema
 


# Manejador correspondiente al comando /reiniciar
def reiniciar(update, context):
        update.message.reply_text("Reiniciando el sistema") # Respondemos al comando con el mensaje
        llamadaSistema("reboot") # Llamada al sistema    
    
def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)


def main():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater("808767729:AAE4gOGYfBxDFOldbnWia34RimXiJWsiQt8", use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))
    dp.add_handler(CommandHandler("ip", ip))
    dp.add_handler(CommandHandler("apagar", apagar))
    dp.add_handler(CommandHandler("reiniciar", reiniciar))
    dp.add_handler(CommandHandler("regar", regar))
    dp.add_handler(CommandHandler("temp", temp))

    # on noncommand i.e message - echo the message on Telegram
    dp.add_handler(MessageHandler(Filters.text, echo))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()


if __name__ == '__main__':
    main()