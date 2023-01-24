from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseNotFound
from django.core.paginator import Paginator
from app import models
from app import forms

OBJECTS_NUM_ON_PAGE = 10

def pagination(objects, page):
    paginator = Paginator(objects, OBJECTS_NUM_ON_PAGE)
    if page < 1 or page > paginator.num_pages:
        return None
    page_content = paginator.get_page(page)
    return page_content


def context_for_sidebar(context):
    context['popular_tags'] = models.Tag.manager.get_top10()
    context['popular_users'] = models.Profile.manager.get_top5()


def index(request, page_num = 1):
    questions_for_page = pagination(models.Question.manager.get_newest(), page_num)
    if questions_for_page == None:
        return HttpResponseNotFound(f"Нет такой страницы")

    context = { 'questions': questions_for_page,
                'title': 'New questions',
                'page_num': page_num,
                'page_url': "index_page",
                # 'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'index.html', context=context)


def tag(request, tag_title : str, page_num = 1):
    questions = models.Question.manager.get_by_tag_name(tag_title)
    if questions == None:
        return HttpResponseNotFound(f"Такого тега не существует")
    elif questions.count() == 0:
        return HttpResponseNotFound(f"Нет вопросов для этого тега")

    questions_for_page = pagination(questions, page_num)
    if questions_for_page == None:
        return HttpResponseNotFound(f"Нет такой страницы")
    
    tag = models.Tag.manager.get(name=tag_title)

    context = { 'questions': questions_for_page,
                'tag': tag,
                'title': "{} ({} Questions) ".format(tag_title, tag.questions.count()),
                'page_num': page_num,
                'page_url': "tag_page",
                # 'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'index.html', context=context)


def hot(request, page_num = 1):
    questions_for_page = pagination(models.Question.manager.get_top(), page_num)
    if questions_for_page == None:
        return HttpResponseNotFound(f"Нет такой страницы")
    context = { 'questions': questions_for_page,
                'title': 'HOT questions',
                'page_num': page_num,
                'page_url': 'hot_page',
                # 'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'index.html', context=context)


def question(request, question_id : int, page_num = 1):
    # question = get_object_or_404(models.Question, id=question_id)
    question = models.Question.manager.get_by_id_or_None(question_id)
    if question == None:
        return HttpResponseNotFound("Нет такого вопроса")

    answers_for_page = pagination(models.Answer.manager.get_by_question(question), page_num)
    if answers_for_page == None:
        return HttpResponseNotFound(f"Нет такой страницы")

    context = { 'title': question.title,
                'question': question,
                'answers': answers_for_page,
                'page_num': page_num,
                'page_url': "question_page",
                # 'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'question.html' , context=context)


def ask(request):
    context = { 'title': 'New question',
                # 'autentificated': True 
    }
    context_for_sidebar(context)

    return render(request, 'ask.html', context=context)

def signup(request):
    context = { 'title': 'Sign up' }
    context_for_sidebar(context)

    return render(request, 'signup.html', context=context)

def login(request):
    if request.method == 'GET':
        user_form = forms.LoginForm()


    context = { 'title': 'Sign in' }
    context_for_sidebar(context)

    return render(request, 'login.html', context=context)
