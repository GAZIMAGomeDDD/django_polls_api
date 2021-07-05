from django.http import HttpResponse, JsonResponse, HttpRequest
from django.db.models import F

from .models import Poll, Choice

from .serializers import (
    PollCreateSerializer,
    PollSerializer,
    GetResultSerializer
)

from rest_framework.decorators import api_view

from typing import Union


@api_view(['GET', 'POST'])
def create_poll_view(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse('Not Implemented\n', status=404)
    
    serializer = PollCreateSerializer(data=request.data)

    if serializer.is_valid():
        poll_text = serializer.data['poll_text']
        choices = serializer.data['choices']
        poll = Poll.objects.create(poll_text=poll_text)

        for choice_text in choices:
            Choice.objects.create(
                poll=poll,
                choice_text=choice_text
            )

        return HttpResponse('Good!\n', status=201)


@api_view(['GET', 'POST'])
def poll_view(request: HttpRequest) -> HttpResponse:
    if request.method != 'POST':
        return HttpResponse('Not Implemented\n', status=404)
    
    serializer = PollSerializer(data=request.data)
 
    if serializer.is_valid():
        poll_id = serializer.data['poll_id']
        choice_id = serializer.data['choice_id']

        Poll.objects.get(id=poll_id).choices.filter(id=choice_id).update(votes=F('votes') + 1)

        return HttpResponse('Good!\n', status=201)


@api_view(['GET', 'POST'])
def get_result(request: HttpRequest) -> Union[JsonResponse, HttpResponse]:
    if request.method != 'POST':
        return HttpResponse('Not Implemented\n', status=404)
    
    serializer = GetResultSerializer(data=request.data)

    if serializer.is_valid():
        lst = []
        poll_id = serializer.data['poll_id']    

        try:
            for choice_data in Poll.objects.get(id=poll_id).choices.values():
                lst.append(choice_data)
        except Poll.DoesNotExist:
            return HttpResponse('Not Implemented\n', status=404)
            
        return JsonResponse({'data': lst}, status=200)
