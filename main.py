import logging
import os
from googlesearch import search

APP_NAME = "https://il-servitore.herokuapp.com/"
TOKEN = "1568387409:AAHzWMtLieiNtzbQcCRyqXI9zsL3oV5BjiQ"

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

logger = logging.getLogger(__name__)

PORT = int(os.environ.get('PORT', '8443'))
# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update, context):
    """Send a message when the command /start is issued."""
    update.message.reply_text('Hi!')


def help(update, context):
    """Send a message when the command /help is issued."""
    update.message.reply_text('You said Help!')


"""Classify the message"""
def category(message_text):
    # return 1 # General
    # return 2 # IIT Mandi
    return 3 # Programming


def reply(update, context):
    """Reply to user message."""
    answer = update.message.text
    if category(update.message.text) != 1:
        result = google_search(update.message.text, 1)
        if result != "":
            update.message.reply_text(f"{answer}\n\nFor more details, refer to {result}")
        else:
            update.message.reply_text(answer)
    else:
        update.message.reply_text(answer)


def error(update, context):
    """Log Errors caused by Updates."""
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def google_search(query, max_results=1):

    result=""

    for j in search(query, tld="co.in", num=max_results, stop=max_results, pause=2): 
        result += j + "\n"

    return result


def start_bot():
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        TOKEN, use_context=True)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # on different commands - answer in Telegram
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # on noncommand i.e message - reply to message on Telegram
    dp.add_handler(MessageHandler(Filters.text, reply))

    # log all errors
    dp.add_error_handler(error)

    # Start the Bot
    updater.start_webhook(listen="0.0.0.0",
                          port=PORT,
                          url_path=TOKEN)
    # updater.bot.set_webhook(url=settings.WEBHOOK_URL)
    updater.bot.set_webhook(APP_NAME + TOKEN)

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    updater.idle()