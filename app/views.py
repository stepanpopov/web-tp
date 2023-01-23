from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from app import models


def context_for_sidebar(context):
    context['popular_tags'] = models.Tag.manager.get_top10()
    context['popular_users'] = models.Profile.manager.get_top5()


def index(request):
    context = { 'questions': models.Question.manager.get_newest(),
                'title': 'New questions',
                'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'index.html', context=context)


def tag(request, tag_title : str):
    questions = models.Question.manager.get_by_tag_name(tag_title)
    if questions == None:
        return HttpResponseNotFound(f"Такого тега не существует")
    elif questions.count() == 0:
        return HttpResponseNotFound(f"Нет вопросов для этого тега")
    

    context = { 'questions': questions,
                'title': tag_title,
                'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'index.html', context=context)


def hot(request):
    context = { 'questions': models.Question.manager.get_top(),
                'title': 'HOT questions',
                'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'index.html', context=context)


def question(request, question_id : int):
    question = get_object_or_404(models.Question, id=question_id)

    if question == None:
        return HttpResponseNotFound("Нет такого вопроса")

    context = { 'title': question.title,
                'question': question,
                'answers': models.Answer.manager.get_by_question(question),
                'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'question.html' , context=context)


def ask(request):
    context = { 'title': 'New question',
                'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'ask.html', context=context)

def signup(request):
    context = { 'title': 'Sign up' }
    context_for_sidebar(context)

    return render(request, 'signup.html', context=context)

def login(request):
    context = { 'title': 'Sign in' }
    context_for_sidebar(context)

    return render(request, 'login.html', context=context)
