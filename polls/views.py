from django.http import HttpResponse, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F

from .models import Poll, Choice

from typing import Union
import json


@csrf_exempt
def create_poll_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        poll_text = request.POST['poll_text']
        choices = json.loads(request.POST['choices'])
        poll = Poll.objects.create(poll_text=poll_text)

        for choice_text in choices:
            Choice.objects.create(
                poll=poll,
                choice_text=choice_text
            )

        return HttpResponse('Good!\n', status=201)
    return HttpResponse('Not Implemented\n', status=404)


@csrf_exempt
def poll_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        poll_id = int(request.POST['poll_id'])
        choice_id = int(request.POST['choice_id'])

        Poll.objects.get(id=poll_id).choices.filter(id=choice_id).update(votes=F('votes') + 1)

        return HttpResponse('Good!\n', status=201)
    return HttpResponse('Not Implemented\n', status=404)


@csrf_exempt
def get_result(request: HttpRequest) -> Union[JsonResponse, HttpResponse]:
    if request.method == 'POST':
        lst = []
        poll_id = int(request.POST['poll_id'])

        try:
            for choice_data in Poll.objects.get(id=poll_id).choices.values():
                lst.append(choice_data)
        except Poll.DoesNotExist:
            return HttpResponse('Not Implemented\n', status=404)
        
        return JsonResponse({'data': lst}, status=200)
    return HttpResponse('Not Implemented\n', status=404)
