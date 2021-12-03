from django.urls import path

from .views import *

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('words/<str:part_of_speech>', AllWordsByPartOfSpeech.as_view(), name='words_by_parts_of_speech'),
    path('api/get-random-test', RandomTestAPI.as_view())
]
