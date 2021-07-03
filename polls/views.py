from django.http import HttpResponse, Http404, JsonResponse, HttpRequest
from django.views.decorators.csrf import csrf_exempt
from .models import Poll, Choice
from django.db.models import F
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

        return HttpResponse('Good!')
    return HttpResponse('Not Implemented')


@csrf_exempt
def poll_view(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST':
        poll_id = int(request.POST['poll_id'])
        choice_id = int(request.POST['choice_id'])

        Poll.objects.get(id=poll_id).choices.filter(id=choice_id).update(votes=F('votes') + 1)

        return HttpResponse('Good!')
    return HttpResponse('Not Implemented')
