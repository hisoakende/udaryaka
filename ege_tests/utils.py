from django.core.exceptions import ObjectDoesNotExist

from .models import *

parts_of_speech_en = ['noun', 'adjective', 'verb', 'participle', 'gerunds', 'adverb']
parts_of_speech_ru_plural = ['существительные', 'прилагательные', 'глаголы', 'причастия', 'деепричастия', 'наречия']
vowels = ['а', 'у', 'о', 'и', 'э', 'ы', 'я', 'ю', 'е', 'ё']


def get_part_of_speech_ru_plural(p):
    return parts_of_speech_ru_plural[parts_of_speech_en.index(p)]


def get_test(test_id=False, number_of_required=10):
    """Возвращает тест - случайный или существующий"""
    if test_id:
        words = [x.word for x in UsersTest.objects.get(test_id=test_id).get_words.all()]
    else:
        words = WordFromDictionary.objects.random(number_of_required)
        if len(set(words)) != number_of_required:
            return get_test(number_of_required=number_of_required)
    return parsed_words(words)


def parsed_words(words):
    """Возвращает распарсенные слова"""
    words_pars = dict()
    index = 0
    for word in words:
        possible_values = []
        correct_value = 0
        for char_i in range(len(word.word)):
            if word.word[char_i] in vowels:
                if char_i == word.accented_character - 1:
                    correct_value = len(possible_values)
                possible_values.append(word.word[:char_i] + word.word[char_i].upper() + word.word[char_i + 1:])
        words_pars[index] = {'possible_values': possible_values, 'correct_value': correct_value}
        index += 1
    return words_pars


def check_test_for_existence(test_id):
    return 200 if UsersTest.objects.filter(test_id=test_id) else 204


def check_user_answers(test_id, data_request):
    """Проверяет пользовательские ответы"""
    words = get_test(test_id).values()
    correct_words = [x['possible_values'][x['correct_value']] for x in words]
    checked_answers = []
    correct_count = 0
    for i in range(len(words)):
        correct = correct_words[i] == data_request[f'question-{i}']
        if correct:
            correct_count += 1
        checked_answers.append((data_request[f'question-{i}'], correct))
    return checked_answers, f'{correct_count}/{len(checked_answers)}'


def added_incorrect_mark(words, user_answers):
    """Добавление пометки об неправильном ответе пользователя"""
    for i in range(len(words)):
        if user_answers[0][i][1]:
            continue
        for value in words[i]['possible_values']:
            if value == user_answers[0][i][0]:
                words[i]['user_incorrect_value'] = words[i]['possible_values'].index(value)
    return words
