from django.db import models

import numpy as np

class Question(models.Model):
    content = models.TextField()
    title = models.CharField(max_length=200)


class Hint(models.Model):
    content = models.TextField()
    yes_votes = models.IntegerField(default=0)
    no_votes = models.IntegerField(default=0)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)

    def sample_from_beta(self, size=1):
        return np.random.beta(self.yes_votes + 1, self.no_votes + 1, size=size)
