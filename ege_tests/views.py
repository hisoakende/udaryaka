from django.http import HttpResponse
from django.views.generic import TemplateView, ListView
from rest_framework.response import Response
from rest_framework.views import APIView

from ege_tests.models import WordFromDictionary
from ege_tests.utils import *


class Homepage(TemplateView):
    """Отображение главной страницы"""
    template_name = 'homepage.html'


def f(request, test_id):
    return HttpResponse(f'{test_id}')


class RandomTestAPI(APIView):
    """Обработка запроса на получение слов для случайного теста"""

    def get(self, request):
        return Response(get_random_test())


class CheckTestForExistence(APIView):
    """Проверка теста на существование"""

    def get(self, request, test_id):
        return Response(status=check_test_for_existence(test_id))


class AllWordsByPartOfSpeech(ListView):
    """Отоброжение всех слов или по конкретной части речи"""
    template_name = 'words.html'
    model = WordFromDictionary
    context_object_name = 'words'

    def get(self, request, *args, **kwargs):
        if self.kwargs['part_of_speech'] in parts_of_speech_en:
            return super().get(request, *args, **kwargs)
        else:
            return HttpResponse(status=404)

    def get_queryset(self):
        words = WordFromDictionary.objects.filter(part_of_speech=self.kwargs['part_of_speech'])
        for x in words:
            index = x.accented_character - 1
            x.word = x.word[:index] + x.word[index].upper() + x.word[index + 1:]
        return words

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['part_of_speech_topic'] = get_part_of_speech_ru_plural(self.kwargs['part_of_speech'])
        return context
