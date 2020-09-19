"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from personal.views import (
    home_screen_view,
    user_homepage_view,
)
from account.views import (
    registration_view,
    logout_view,
    login_view,
    account_view,
)
from books.views import (
    books_insert,
    search_view,
    add_to_collection,
    book_view,
    user_view,
    books_list_view
)

from usercollections.views import (
    collections_view,
    collection_view,
    book_delete,
    collection_delete,
    collection_update,
    recentAdd_view,
    add_book_to_collection,
    collection_add,
)

from review.views import (
    add_review,
)

from AdvSearch.views import (
    adv_search_book,
    adv_search_user,
    adv_search_collection,
    adv_search_review,
)

from goals.views import (
    goal_view,
    goal_detail_view,
    edit_goal_view,
    goal_delete_view,
    record_books_read,
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_screen_view,name="home"),
    path('user_homepage/', user_homepage_view,name='user_homepage'),
    path('register/',registration_view, name='register'),
    path('logout/',logout_view, name='logout'),
    path('login/',login_view,name='login'),
    path('account/',account_view,name='account'),
    path('books_insert/',books_insert, name="books_insert"),
    path('books_list/',books_list_view, name="books_list"),
    path('search/', search_view, name='search_results'),
    path('setGoal/',goal_view,name='setGoal'),
    path('goalDetail/',goal_detail_view,name='goalDetail'),
    path('editGoal/',edit_goal_view,name='editGoal'),
    path('deleteGoal/',goal_delete_view,name='deleteGoal'),
    path('record_books_read/<str:book_id>/',record_books_read,name='record_books_read'),
    path('collections/', collections_view, name="collections"),
    path('addToCollection/<isbn>/<col>',add_to_collection,name="addToCollection"),
    path('collection/<str:collection_id>/', collection_view, name="collection"),
    path('collection/showRecent', recentAdd_view, name="showRecent"),
    path('collection_delete_book/<str:collection_id>/<str:book_id>/', book_delete, name="collection_delete_book"),
    path('collection_add/', collection_add, name="collection_add"),
    path('collection_delete/', collection_delete, name="collection_delete"),
    path('collection_update/', collection_update, name="collection_update"),
    path('password_change/done/',
         auth_views.PasswordChangeDoneView.as_view(template_name='registration/password_change_done.html'),
         name='password_change_done'),

    path('password_change/', auth_views.PasswordChangeView.as_view(template_name='registration/password_change.html'),
         name='password_change'),

    path('password_reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_done.html'),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view
        (template_name='registration/password_reset.html'),
         name='password_reset_confirm'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete.html'),
         name='password_reset_complete'),
    path('book/<str:isbn>/', book_view, name='book'),
    path('user_profile/<str:username>/', user_view, name='user_profile'),
    path('add_review/', add_review, name="add_review"),
    path('add_book_btn/', add_book_to_collection, name="add_book_btn"),
    path('adv_search_book/', adv_search_book, name="adv_search_book"),
    path('adv_search_user/', adv_search_user, name="adv_search_user"),
    path('adv_search_collection/', adv_search_collection, name="adv_search_collection"),
    path('adv_search_review/', adv_search_review, name="adv_search_review"),
] + static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)