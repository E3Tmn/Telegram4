import os
import random

import redis
from dotenv import load_dotenv
from telegram import ReplyKeyboardMarkup, Update
from telegram.ext import (CallbackContext, CommandHandler, ConversationHandler,
                          Filters, MessageHandler, Updater)

from quiz import get_quiz

QUESTION, ANSWER, FOLD = range(3)


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
    return QUESTION


def handle_new_question_request(update: Update, context: CallbackContext, db, quiz):
    question, answer = random.choice(list(quiz.items()))
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=question
    )
    context.user_data["answer"] = answer
    success = db.set(update.effective_chat.id, question)
    print(answer)
    return FOLD


def handle_solution_attempt(update: Update, context: CallbackContext):
    answer = context.user_data["answer"]
    print(answer)
    if update.message.text == answer:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»'
        )

    else:
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='Неправильно… Попробуешь ещё раз?'
        )
    return QUESTION


def handle_fold_button(update: Update, context: CallbackContext):
    if update.message.text != 'Сдаться':
        return handle_solution_attempt(update, context)
    answer = context.user_data["answer"]
    context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=answer
        )
    return QUESTION


def echo(update: Update, context: CallbackContext):
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text='bye'
        )


def main():
    quiz = get_quiz()
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

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            QUESTION: [MessageHandler(
                    Filters.text,
                    lambda update, context:handle_new_question_request(update, context, db, quiz)
                )
            ],
            ANSWER: [MessageHandler(Filters.text, handle_solution_attempt)],
            FOLD: [MessageHandler(Filters.text, handle_fold_button)]
        },
        fallbacks=[CommandHandler('cancel', echo)]
    )
    dispatcher.add_handler(conv_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
