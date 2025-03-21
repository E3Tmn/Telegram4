import os
import random

import vk_api as vk
from dotenv import load_dotenv
from vk_api.keyboard import VkKeyboard
from vk_api.longpoll import VkEventType, VkLongPoll

from quiz import get_quiz

user_data = {}


def send_message(event, vk_api, keyboard, text='Привет'):
    vk_api.messages.send(
            user_id=event.user_id,
            message=text,
            keyboard=keyboard.get_keyboard(),
            random_id=random.randint(1, 1000)
        )


def echo(event, vk_api, keyboard, quiz):
    if event.text == 'Привет':
        send_message(event, vk_api, keyboard)
    elif event.text == 'Новый вопрос':
        question, answer = random.choice(list(quiz.items()))
        send_message(event, vk_api, keyboard, question)
        user_data["answer"] = answer
    elif event.text == 'Сдаться':
        answer = user_data["answer"]
        send_message(event, vk_api, keyboard, answer)
    elif event.text == user_data["answer"]:
        send_message(event, vk_api, keyboard, 'Правильно! Поздравляю! Для следующего вопроса нажми «Новый вопрос»')
    else:
        send_message(event, vk_api, keyboard, 'Неправильно… Попробуешь ещё раз?')


def main():
    load_dotenv()
    quiz = get_quiz()
    vk_session = vk.VkApi(token=os.environ["VK_TOKEN"])
    vk_api = vk_session.get_api()
    keyboard = VkKeyboard(one_time=True)

    keyboard.add_button('Новый вопрос')
    keyboard.add_button('Сдаться')

    keyboard.add_line()
    keyboard.add_button('Мой счет')
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api, keyboard, quiz)


if __name__ == "__main__":
    main()
