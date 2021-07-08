from rest_framework import serializers
from .models import Poll, Choice


class ChoiceSerializer(serializers.ModelSerializer):
    choice_text = serializers.CharField(max_length=256)

    class Meta:
        model = Choice
        fields = ('id', 'choice_text')


class CreatePollSerializer(serializers.ModelSerializer):

    poll_text = serializers.CharField(max_length=256)
    choices = ChoiceSerializer(many=True)

    class Meta:
        model = Poll
        fields = '__all__'

    def create(self, validated_data: dict) -> Poll:

        choices = validated_data.get('choices')
        instance = Poll.objects.create(
            poll_text=validated_data.get('poll_text'))

        Choice.objects.bulk_create([
            Choice(
                poll=instance,
                choice_text=data['choice_text']
            ) for data in choices
        ])

        return instance


class PollSerializer(serializers.Serializer):

    poll_id = serializers.IntegerField()
    choice_id = serializers.IntegerField()


class GetResultSerializer(serializers.Serializer):

    poll_id = serializers.IntegerField()
