from django.shortcuts import render,redirect
from account.models import Account
from books.models import Books
from goals.models import Goal
from django.http import HttpResponseRedirect
import random
from django.views.generic import ListView
from usercollections.models import Collection
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import datetime

def home_screen_view(request):
    '''
    home page to display books using pagination 
    '''
    context = {}
    paginate_num = 20
    books = Books.objects.all()
    user = request.user
    paginator = Paginator(books, paginate_num)
    page = request.GET.get('page',1)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)
    index = books.number-1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    context['books'] = books
    context['page_range'] = page_range
    context['max_index'] = max_index

    if user.is_authenticated:
        return redirect("user_homepage")
    
    return  render(request, "personal/home.html",context)

    
def user_homepage_view(request):
    '''
    user home page consists of user profile link on top left
    all user collections
    reading goal
    similar users
    other user collecitions
    personalised recommendation
    popular book recommendation
    random books
    '''
    context = {}
    books = Books.objects.all()
    new_books = Books.objects.all()
    if len(list(books)) > 4:
        books=random.sample(list(books),4)
    user = request.user
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    context['hide'] = False
    if user.is_authenticated:
        paginator = Paginator(books,8)
        page = request.GET.get('page',1)
        try:
            books = paginator.page(page)
        except PageNotAnInteger:
            books = paginator.page(1)
        except EmptyPage:
            books = paginator.page(paginator.num_pages)
        context['username'] = user.username
        uid = Account.objects.get(username=user.username).id
        goals = Goal.objects.filter(UID=uid,year=current_year,month=current_month)
        if goals.exists():
            context['hide'] = True
            context['numBooks'] = goals[0].numBooks
            context['numFinished'] = goals[0].numFinished
            percentage = goals[0].numFinished / goals[0].numBooks * 100
            context['percentage'] = round(percentage)
        collections = Collection.objects.filter(UID=uid)
        users=Account.objects.exclude(username=user.username)
        other_users_collection=Collection.objects.none()
        for user in users:
            uid = Account.objects.get(username=user.username).id
            other_users_collection=Collection.objects.filter(UID=uid) | other_users_collection

        other_users_collection=list(other_users_collection)
        if len(other_users_collection) >=4:
            other_users_collection=random.sample(other_users_collection,4)
        else: 
            other_users_collection=random.sample(other_users_collection,len(other_users_collection))

        # Similar Users
        if Account.objects.get(username=request.user.username).similar_users:
            similar_users = Account.objects.get(username=request.user.username).similar_users.split('/')[:-1]
        else:
            similar_users = []
        context['similar_user'] = similar_users

        # Similar Users' Books
        similar_user_books = []
        for u in similar_users:
            col = Collection.objects.get(UID=Account.objects.get(username=u), collectionName='Read')
            for b_k in col.books.all():
                if b_k not in similar_user_books:
                    similar_user_books.append(b_k)
        context['similar_user_books'] = similar_user_books

        context['collections'] = collections
        context['books'] = books
        context['uid'] = user.id
        context['other_users_collection'] = other_users_collection
        #similar books
        fiction = list(new_books.filter(genres__contains='Fiction').order_by('?')[:10])
        thriller = list(new_books.filter(genres__contains='Thriller').order_by('?')[:10])
        great = list(new_books.filter(genres__contains='Literature').order_by('?')[:10])
        context['Fiction'] = fiction
        context['Thriller'] = thriller
        context['Great'] = great

        books_ISBN_list=[]
        books_count={}
        recommedation_list=[]
        collections = Collection.objects.exclude(UID=uid)
        collections=list(collections)
        for collection in collections:
            for book in collection.books.all():
                books_ISBN_list.append(book.ISBN)
        for book_ISBN in books_ISBN_list:
            books_count[book_ISBN]=books_ISBN_list.count(book_ISBN)
        books_count_sort=sorted(books_count.items(), key=lambda x : x[1],reverse=True)

        for books_count in books_count_sort:
            recommedation_list.append(books_count[0])
        recommedation_bname=Books.objects.none()
        for isbn in recommedation_list:
            recommedation_bname=Books.objects.filter(ISBN=isbn) | recommedation_bname

        context["recommedation_bname"]=recommedation_bname

        return  render(request, "personal/user_homepage.html",context)
    else:
        return redirect("home")
