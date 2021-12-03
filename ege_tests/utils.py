from .models import WordFromDictionary


parts_of_speech_en = ['noun', 'adjective', 'verb', 'participle', 'gerunds', 'adverb']
parts_of_speech_ru_plural = ['существительные', 'прилагательные', 'глаголы', 'причастия', 'деепричастия', 'наречия']
vowels = ['а', 'у', 'о', 'и', 'э', 'ы', 'я', 'ю', 'е', 'ё']


def get_part_of_speech_ru_plural(p):
    return parts_of_speech_ru_plural[parts_of_speech_en.index(p)]


def get_random_test(number_of_required=10):
    """Возвращает слова для случайного тест для API"""
    words = WordFromDictionary.objects.random(number_of_required)
    result = dict()
    index = 0
    for word in words:
        possible_values = []
        correct_value = 0
        for char_i in range(len(word.word)):
            if word.word[char_i] in vowels:
                if char_i == word.accented_character - 1:
                    correct_value = len(possible_values)
                possible_values.append(word.word[:char_i] + word.word[char_i].upper() + word.word[char_i+1:])
        result[index] = {'possible_values': possible_values, 'correct_value': correct_value}
        index += 1
    return result
