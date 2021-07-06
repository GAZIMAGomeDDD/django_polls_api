from rest_framework import serializers


class CreatePollSerializer(serializers.Serializer):

    poll_text = serializers.CharField(max_length=256)
    choices = serializers.ListField(
        child=serializers.CharField(max_length=256), 
        allow_empty=False
    )


class PollSerializer(serializers.Serializer):

    poll_id = serializers.IntegerField()
    choice_id = serializers.IntegerField()


class GetResultSerializer(serializers.Serializer):

    poll_id = serializers.IntegerField()
