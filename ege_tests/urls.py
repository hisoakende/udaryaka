from django.urls import path

from .views import *

urlpatterns = [
    path('', Homepage.as_view(), name='homepage'),
    path('words/<str:part_of_speech>', AllWordsByPartOfSpeech.as_view(), name='words_by_parts_of_speech'),
    path('tests/id=<int:test_id>', UsersTestPage.as_view(), name='users_test'),

    path('api/get-random-test', RandomTestAPI.as_view()),
    path('api/check_test_for_existence/<int:test_id>', CheckTestForExistence.as_view())
]
