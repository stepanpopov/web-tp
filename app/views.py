from django.shortcuts import render
from django.http import HttpResponseNotFound
from app import models

def index(request):
    context = { 'questions': models.QUESTIONS,
                'title': 'New questions',
                'popular_tags': models.POPULAR_TAGS,
                'popular_users': models.POPULAR_USERS 
    }

    return render(request, 'index.html', context=context)

def tag(request, tag_title : str):
    questions = []
    for question in models.QUESTIONS:
        if tag_title in question['tags']:
            questions.append(question)
    if len(questions) == 0:
        return HttpResponseNotFound("404")

    context = { 'questions': questions,
                'title': tag_title,
                'popular_tags': models.POPULAR_TAGS,
                'popular_users': models.POPULAR_USERS 
    }

    return render(request, 'index.html', context=context)

def hot(request):
    context = { 'questions': models.HOT_QUESTIONS,
                'title': 'HOT questions',
                'popular_tags': models.POPULAR_TAGS,
                'popular_users': models.POPULAR_USERS 
    }

    return render(request, 'index.html', context=context)

def question(request, question_id : int):
    question_needed = None
    for question in models.QUESTIONS:
        if question['id'] == question_id:
            question_needed = question

    if question_needed == None:
        return HttpResponseNotFound("404")


    context = { 'title': 'Question {}'.format(question_id),
                'question': question_needed,
                'answers': models.ANSWERS[question_id],
                'popular_tags': models.POPULAR_TAGS,
                'popular_users': models.POPULAR_USERS 
    }

    return render(request, 'question.html' , context=context)

def ask(request):
    context = { 'title': 'New question',
                'popular_tags': models.POPULAR_TAGS,
                'popular_users': models.POPULAR_USERS 
    }

    return render(request, 'ask.html', context=context)

def signup(request):
    context = { 'title': 'Sign up',
                'popular_tags': models.POPULAR_TAGS,
                'popular_users': models.POPULAR_USERS 
    }

    return render(request, 'signup.html', context=context)

def login(request):
    context = { 'title': 'Sign in',
                'popular_tags': models.POPULAR_TAGS,
                'popular_users': models.POPULAR_USERS 
    }

    return render(request, 'login.html', context=context)
