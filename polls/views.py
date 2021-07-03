from django.http import HttpResponse, Http404, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Poll, Choice
import json


@csrf_exempt
def create_poll_view(request):

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
