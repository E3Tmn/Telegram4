from collections import defaultdict


def get_quiz():
    text = ''
    with open('questions/1vs1200.txt', 'r', encoding='KOI8-R') as file:
        text = file.read().split('\n\n')

    quiz = defaultdict(str)
    for i, line in enumerate(text):
        if 'Ответ' in line:
            quiz[text[i-1].split(":", 1)[-1]] = line.replace('Ответ:', '').strip()

    return quiz
