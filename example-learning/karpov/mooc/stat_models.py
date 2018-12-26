from django.db.models import Sum

import numpy as np


class HintSelector():
    def __init__(self, question):
        self.q = question

    def thompson_sampling_strategy(self):
        hints = self.q.hint_set.all()
        chosen_score = -1
        chosen = None
        for hint in hints:
            sample = hint.sample_from_beta()
            if sample > chosen_score:
                chosen_score = sample
                chosen = hint
        return chosen 



class QuestionSelector():
    def __init__(self, questions, hint_model):
        self.qs = questions
        self.hint_model = hint_model

    def select_question(self, num_samples):
        for q in self.qs:
            if q.hint_set.count() == 0:
                return q

        all_votes_count = self.hint_model.objects.aggregate(
                Sum('yes_votes'), Sum('no_votes')
                )
        all_yes_votes = all_votes_count['yes_votes__sum'] or 0
        all_no_votes = all_votes_count['no_votes__sum'] or 0

        
        samples_of_expeected_hint = np.random.beta(all_yes_votes + 1,
                all_no_votes + 1, size=(num_samples, 1))

        chosen_question = None
        times_won = 0
        
        
        for q in self.qs:
            matrix_of_all_samples = np.zeros(shape=(num_samples, 0))
            matrix_of_all_samples = np.append(matrix_of_all_samples,
                    samples_of_expeected_hint, axis=1)
            for hint in q.hint_set.all():
                matrix_of_all_samples = np.append(matrix_of_all_samples,
                        hint.sample_from_beta(size=(num_samples, 1)), axis=1)
            
            eq = matrix_of_all_samples.max(axis=1) == samples_of_expeected_hint
            times_won_this_q = eq.sum()
            if times_won_this_q > times_won:
                times_won = times_won_this_q
                chosen_question = q

        return chosen_question
