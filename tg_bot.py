import os

import redis
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, Filters,
                          MessageHandler, Updater)

from quiz import get_question


def start(update: Update, context: CallbackContext) -> None:
    custom_keyboard = [
        ['Новый вопрос', 'Сдаться'],
        ['Мой счет']
    ]
    reply_markup = ReplyKeyboardMarkup(custom_keyboard)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Привет! Я бот для викторин!",
        reply_markup=reply_markup
    )


def echo(update: Update, context: CallbackContext, db):
    if update.message.text == 'Новый вопрос':
        question = get_question()
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=question
        )
        success = db.set(update.effective_chat.id, question)
        print(db.get(update.effective_chat.id))


def main():
    load_dotenv()
    db = redis.Redis(
        host='redis-13330.c15.us-east-1-2.ec2.redns.redis-cloud.com',
        port=13330,
        decode_responses=True,
        username=os.environ['REDIS_USERNAME'],
        password=os.environ['REDIS_PASSWORD'],
    )

    updater = Updater(token=os.environ['TELEGRAM_TOKEN'], use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    echo_handler = MessageHandler(
        Filters.text & (~Filters.command),
        lambda update, context: echo(update, context, db)
    )
    dispatcher.add_handler(echo_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
