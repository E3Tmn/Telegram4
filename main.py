from collections import defaultdict


def main():
    text = ''
    with open('questions/1vs1200.txt', 'r', encoding='KOI8-R') as file:
        text = file.read().split('\n\n')

    questions = defaultdict(str)
    for i, line in enumerate(text):
        if 'Ответ' in line:
            questions[text[i-1]] = line

    # for key, value in questions.items():
    #     print(key, value)


if __name__ == '__main__':
    main()
