from django.urls import path
from . import views
from django.views.decorators.cache import never_cache

urlpatterns = [
    path('register/', views.register, name="register"),
    path('', never_cache(views.login), name="login"), # does not save js / css in cache for this url
    path('timer/', views.set_timer, name='timer'),
    path('question-hub/', never_cache(views.question_hub), name='question-hub'), # does not save js / css in cache for this url
    path('question/<int:pk>', never_cache(views.coding_page), name='coding-page'), # does not save js / css in cache for this url
    path('submissions-page/', never_cache(views.submission_page), name='submissions-page'), # does not save js / css in cache for this url
    path('leaderboard/', never_cache(views.leaderboard), name='leaderboard'), # does not save js / css in cache for this url
    path('logout/', never_cache(views.logout), name='logout'), # does not save js / css in cache for this url
    path('submission_<int:submission_id>/', never_cache(views.view_submission), name='view-submission'), # does not save js / css in cache for this url
    path('load-buffer/', views.load_buffer, name='loadbuffer'),
    path('get-output/', views.get_output, name='get-output'),
    path('cheat/', views.cheat, name='cheat'),
]