parts_of_speech_en = ['noun', 'adjective', 'verb', 'participle', 'gerunds', 'adverb']
parts_of_speech_ru_plural = ['существительные', 'прилагательные', 'глаголы', 'причастия', 'деепричастия', 'наречия']


def get_part_of_speech_ru_plural(p):
    return parts_of_speech_ru_plural[parts_of_speech_en.index(p)]
