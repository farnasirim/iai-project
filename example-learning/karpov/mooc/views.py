from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_http_methods
from django.template import loader

from .models import Question

# Create your views here.

def index(request):
    questions_list = Question.objects.all()
    template = loader.get_template('mooc/index.html')

    context = {
        'questions_list': questions_list,
    }

    return HttpResponse(template.render(context, request))


def question(request, question_id):
    question = Question.objects.get(pk=question_id)
    selected_hint = question.hint_set.first()  # TODO: fix selection
    context = {
        'question': question,
        'hint': selected_hint,
    }

    return render(request, 'mooc/question.html', context)


@require_http_methods(["POST"])
def vote(request, question_id, hint_id):
    vote = 'yes' in request.POST
    print(vote)
    return render(request, 'mooc/thanks.html', {})


@require_http_methods(["POST", "GET"])
def add_hint(request):
    if request.method == "POST":
        qid = int(request.POST['question_id'][0])
        selected_question = Question.objects.get(id=qid)
        hint = selected_question.hint_set.create(
                content=request.POST['hint'],
                )
        context = {
                'hint': hint,
                'question': selected_question,
                }
        return render(request, 'mooc/hint_added.html', context)
    elif request.method == "GET":
        # TODO: select question
        question = Question.objects.first()
        return render(request, 'mooc/add_hint.html', {'question': question})
    else:
        raise PermissionDenied
