from django.contrib import admin
from django.urls import path
from app import views

from django.conf.urls.static import static
from technochan import settings

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.index, name='index'),
    path('page/<int:page_num>', views.index, name='index_page'),

    path('question/<int:question_id>', views.question, name='question'),
    path('question/<int:question_id>/page/<int:page_num>', views.question, name='question_page'), 

    path('tag/<str:tag_title>', views.tag, name='tag'),
    path('tag/<str:tag_title>/page/<int:page_num>', views.tag, name='tag_page'),

    path('hot', views.hot, name='hot'),
    path('hot/page/<int:page_num>', views.hot, name='hot_page'),

    path('ask', views.ask, name='ask'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login')
]

if settings.DEBUG:
    urlpatterns += (static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS) + static(settings.MEDIA_URL,
                                                                                                  document_root=settings
                                                                                                  .MEDIA_ROOT))
