from django.http import  HttpRequest
from django.db.models import F

from .models import Poll, Choice

from .serializers import (
    CreatePollSerializer,
    PollSerializer,
    GetResultSerializer
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class CreatePoll(APIView):

    def get(self, request: HttpRequest) -> Response:

        return Response(
            'Not Implemented\n', 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def post(self, request: HttpRequest) -> Response:

        serializer = CreatePollSerializer(data=request.data)
        
        if serializer.is_valid():
            poll_text = serializer.data['poll_text']
            choices = serializer.data['choices']
            poll = Poll.objects.create(poll_text=poll_text)

            Choice.objects.bulk_create([
                Choice(
                    poll=poll,
                    choice_text=choice_text
                ) for choice_text in choices
            ])

            return Response(
                data={'success': True}, 
                status=status.HTTP_201_CREATED
            )

        return Response(
            data={'success': False}, 
            status=status.HTTP_400_BAD_REQUEST
        ) 


class PollView(APIView):
    def get(self, request: HttpRequest) -> Response:

        return Response(
            'Not Implemented\n', 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )

    def post(self, request: HttpRequest) -> Response:

        serializer = PollSerializer(data=request.data)
        
        if serializer.is_valid():
            poll_id = serializer.data['poll_id']
            choice_id = serializer.data['choice_id']

            try:
                Poll.objects.get(id=poll_id).choices.filter(id=choice_id).update(votes=F('votes') + 1)

                return Response(
                    data={'success': True}, 
                    status=status.HTTP_201_CREATED
                )
            except Poll.DoesNotExist:
                return Response(
                    data={'success': False}, 
                    status=status.HTTP_400_BAD_REQUEST
                ) 
        return Response(
            data={'success': False}, 
            status=status.HTTP_400_BAD_REQUEST
        )


class GetResult(APIView):

    def get(self, request: HttpRequest) -> Response:

        return Response(
            'Not Implemented\n', 
            status=status.HTTP_405_METHOD_NOT_ALLOWED
        )
    
    def post(self, request: HttpRequest) -> Response:
        serializer = GetResultSerializer(data=request.data)

        if serializer.is_valid():
            data = []
            poll_id = serializer.data['poll_id']    

            try:
                for choice_data in Poll.objects.get(id=poll_id).choices.values():
                    data.append(choice_data)
            except Poll.DoesNotExist:
                return Response({'data': []}, status=status.HTTP_204_NO_CONTENT)
                
            return Response({'data': data}, status=status.HTTP_200_OK)


# @api_view(['GET', 'POST'])
# def create_poll_view(request: HttpRequest) -> HttpResponse:
#     if request.method != 'POST':
#         return HttpResponse('Not Implemented\n', status=404)
    
#     serializer = PollCreateSerializer(data=request.data)

#     if serializer.is_valid():
#         poll_text = serializer.data['poll_text']
#         choices = serializer.data['choices']
#         poll = Poll.objects.create(poll_text=poll_text)

#         Choice.objects.bulk_create([
#             Choice(
#                 poll=poll,
#                 choice_text=choice_text
#             ) for choice_text in choices
#         ])

#         return HttpResponse('Good!\n', status=201)


# @api_view(['GET', 'POST'])
# def poll_view(request: HttpRequest) -> HttpResponse:
#     if request.method != 'POST':
#         return HttpResponse('Not Implemented\n', status=404)
    
#     serializer = PollSerializer(data=request.data)
 
#     if serializer.is_valid():
#         poll_id = serializer.data['poll_id']
#         choice_id = serializer.data['choice_id']

#         Poll.objects.get(id=poll_id).choices.filter(id=choice_id).update(votes=F('votes') + 1)

#         return HttpResponse('Good!\n', status=201)


# @api_view(['GET', 'POST'])
# def get_result(request: HttpRequest) -> Union[JsonResponse, HttpResponse]:
#     if request.method != 'POST':
#         return HttpResponse('Not Implemented\n', status=404)
    
#     serializer = GetResultSerializer(data=request.data)

#     if serializer.is_valid():
#         lst = []
#         poll_id = serializer.data['poll_id']    

#         try:
#             for choice_data in Poll.objects.get(id=poll_id).choices.values():
#                 lst.append(choice_data)
#         except Poll.DoesNotExist:
#             return HttpResponse('Not Implemented\n', status=404)
            
#         return JsonResponse({'data': lst}, status=200)
