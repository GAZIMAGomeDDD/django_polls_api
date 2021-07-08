from django.db.models import F
from django.http.response import Http404

from .models import Poll
from .serializers import (
    CreatePollSerializer,
    PollSerializer,
    GetResultSerializer
)

from rest_framework import generics, viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework.request import Request


class CreatePollViewSet(viewsets.ModelViewSet):

    serializer_class = CreatePollSerializer
    queryset = Poll.objects
    http_method_names = ('post',)


class PollView(mixins.UpdateModelMixin, generics.GenericAPIView):

    serializer_class = PollSerializer

    def get_object(self, pk: int) -> Poll:
        try:
            return Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            raise Http404

    def update(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        poll_id = serializer.data.get('poll_id')
        choice_id = serializer.data.get('choice_id')
        choice = self.get_object(poll_id).choices.filter(id=choice_id)
        
        if choice.count() != 1:
            raise Http404

        choice.update(votes=F('votes') + 1)

        return Response(data={'success': True}, status=status.HTTP_201_CREATED)
        
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.update(request, *args, **kwargs)


class GetResult(mixins.RetrieveModelMixin, generics.GenericAPIView):

    serializer_class = GetResultSerializer

    def get_object(self, pk: int) -> Poll:
        try:
            return Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            raise Http404
        
    def retrieve(self, request: Request, *args, **kwargs) -> Response:
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        poll_id = serializer.data.get('poll_id')
        result = [choice_data for choice_data in self.get_object(poll_id).choices.values()]

        return Response(data={'result': result}, status=status.HTTP_200_OK)
    
    def post(self, request: Request, *args, **kwargs) -> Response:
        return self.retrieve(request, *args, **kwargs)
