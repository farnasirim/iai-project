from django.db import models

class Question(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=200)


class Hint(models.Model):
    content = models.TextField()
    yes_votes = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
