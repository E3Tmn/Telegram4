import random
from collections import defaultdict


def read_file():
    text = ''
    with open('questions/1vs1200.txt', 'r', encoding='KOI8-R') as file:
        text = file.read().split('\n\n')

    quiz = defaultdict(str)
    for i, line in enumerate(text):
        if 'Ответ' in line:
            quiz[text[i-1]] = line

    return quiz


def get_question():
    quiz = read_file()
    return random.choice(list(quiz.keys()))
