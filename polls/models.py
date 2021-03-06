from django.db import models


class Poll(models.Model):

    poll_text = models.CharField(max_length=256)

    def __str__(self):
        return self.poll_text
    
    class Meta:
        db_table = 'poll'


class Choice(models.Model):

    poll = models.ForeignKey(
        to=Poll, 
        on_delete=models.CASCADE,
        related_name='choices'
    )
    choice_text = models.CharField(max_length=256)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text

    class Meta:
        db_table = 'choice'
