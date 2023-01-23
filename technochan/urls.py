from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('question/<int:question_id>', views.question, name='question'),  
    path('ask', views.ask, name='ask'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('tag/<str:tag_title>', views.tag, name='tag'),
    path('hot', views.hot, name='hot')
]
