import csv, io
from django.shortcuts import render, get_object_or_404
from django.contrib import messages
from usercollections.models import Collection
from django.views.generic import TemplateView, ListView, DetailView
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Books
from django.shortcuts import redirect
from account.models import Account
from django.db.models import Q
from django.shortcuts import render,redirect
from review.models import Review
from django.db.models import Avg
import math
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from books.models import Books
from books.forms import BookForm
import datetime
from goals.models import Goal


def books_insert(request):
    '''
    books_insert functions takes the request from the web and gets the user id and allows the user to fill a form
    Form info is updated as a book object
    '''
    context = {}
    user = request.user

    if user.is_authenticated:
        context['uid'] = user.id
        if request.method =='POST':
            form = BookForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
            else:
                context['form'] = form
                return render(request, 'books/books_insert.html', context)
    
    form = BookForm()
    context['form'] = form
    return render(request,'books/books_insert.html', context)


def search_view(request):
    '''
    search_view helps users find the book they are looking for
    pagination helps display and view books clearly
    pagination also satisfies RESTfulness
    '''
    template = 'books/search_results.html'
    paginate_num = 20
    query = request.GET.get('q')
    user = request.user
    if not query:
        query = ""

    books_list = Books.objects.filter(
        Q(title__icontains=query) | Q(language__icontains=query) | Q(authors__icontains=query) | Q(country__icontains=query)
    )
    
    paginator = Paginator(books_list, paginate_num)
    page = request.GET.get('page',1)
    try:
        books_list = paginator.page(page)
    except PageNotAnInteger:
        books_list = paginator.page(1)
    except EmptyPage:
        books_list = paginator.page(paginator.num_pages)
    index = books_list.number-1
    max_index = len(paginator.page_range)
    start_index = index - 3 if index >= 3 else 0
    end_index = index + 3 if index <= max_index else max_index
    page_range = list(paginator.page_range)[start_index:end_index]

    if user.is_authenticated:
        uid = Account.objects.get(username=user.username).id
        collections = Collection.objects.filter(UID=uid)
        context = {
            'books_list': books_list,
            'collections': collections,
            'page_range': page_range,
            'uid': user.id,
            'max_index': max_index,
        }
    else:
        context = {
            'books_list': books_list,
            'page_range': page_range,
            'max_index': max_index,
        }

    _mutable = request.GET._mutable
    request.GET._mutable = True
    if 'page' in request.GET:
        request.GET.pop('page')
    request.GET._mutable = _mutable
    return render(request, template, context)

def book_view(request, isbn):
    '''
    describes book details - including all characteristics in Book model, rating, review, etc
    allows users to keep track of read,want to read and currently reading
    users can also add books to collections here
    '''
    context = {}
    book = get_object_or_404(Books, ISBN=isbn)
    user = request.user
    reviews = Review.objects.filter(BID=book)
    rating = reviews.aggregate(avg_rating=Avg('rating'))['avg_rating']
    number_of_read = Collection.objects.filter(collectionName='Read', books=book).count()
    number_of_want_to_read = Collection.objects.filter(collectionName='Want to Read', books=book).count()
    number_of_currently_reading = Collection.objects.filter(collectionName='Currently Reading', books=book).count()

    if rating != None:
        context['rating'] = round(rating, 1)
        context['rating_fill'] = range(math.floor(rating))
        context['rating_half_fill'] = range(math.ceil(rating) - math.floor(rating))
        context['rating_unfill'] = range(5 - math.ceil(rating))
    else:
        context['rating'] = 'No Rating'

    if user.is_authenticated:
        account = Account.objects.get(username=user.username)
        uid = account.id
        collections = Collection.objects.filter(UID=account)
        context['uid'] = uid
        context['reviews'] = reviews
        context['collections'] = collections
        # similar_user_books
        similar_user_books = []
        if Account.objects.get(username=user.username).similar_users:
            similar_users = Account.objects.get(username=user.username).similar_users.split('/')[:-1]
            for u in similar_users:
                col = Collection.objects.get(UID=Account.objects.get(username=u), collectionName='Read')
                for b_k in col.books.all():
                    if b_k not in similar_user_books and b_k != book:
                        similar_user_books.append(b_k)
        else:
            similar_user_books = []
        context['similar_user_books'] = similar_user_books
    book.genres = ', '.join(book.genres.split('|'))
    context['book'] = book
    context['isbn'] = book.ISBN
    context['number_of_read'] = number_of_read
    context['number_of_want_to_read'] = number_of_want_to_read
    context['number_of_currently_reading'] = number_of_currently_reading

    same_collections = Collection.objects.filter(books=book)
    same_books = Books.objects.filter(collection__in=same_collections).exclude(pk=book).order_by('?')[:10]
    context['same_collection_books'] = list(same_books)

    return render(request, 'books/book.html', context)

def user_view(request,username):
    '''
    describes user profile
    reading goal and collections
    books read and user details like age and gender
    '''
    context = {}
    uid = Account.objects.get(username=username).id
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    goals = Goal.objects.filter(UID=uid, year=current_year, month=current_month)
    user = get_object_or_404(Account, username=username)
    collections = Collection.objects.filter(UID=uid)
    context['collections'] = collections
    context['user'] = user
    context['UID_id'] = uid
    context['uid'] = request.user.id
    if goals.exists():
        # context['hide'] = True
        context['numBooks'] = goals[0].numBooks
        context['numFinished'] = goals[0].numFinished
        percentage = goals[0].numFinished / goals[0].numBooks * 100
        context['percentage'] = round(percentage)
        if context['numFinished'] > 0:
            finished_books = goals[0].books.all()
            context['finished_books'] = finished_books
    try:
        collection = Collection.objects.get(UID=uid,collectionName='Read')
        context['recent_read'] = [book for book in collection.books.all()]
    except:
        context['recent_read'] = None
    try:
        collection = Collection.objects.get(UID=uid,collectionName='Currently Reading')
        context['current_reading'] = [book for book in collection.books.all()]
    except:
        context['current_reading'] = None
    try:
        collection = Collection.objects.get(UID=uid,collectionName='Want to Read')
        context['want_read'] = [book for book in collection.books.all()]
    except:
        context['want_read'] = None

    return render(request, 'books/user_profile.html', context)

#@login_required
def add_to_collection(request,isbn,col):
    '''
    allows user to add books to preset collection or a named collection
    '''
    context = {}
    book = get_object_or_404(Books, ISBN=isbn)
    user = request.user
    if user.is_authenticated:
        uid = Account.objects.get(username=user.username).id
        collection = Collection.objects.filter(id=col)

        context['uid'] = uid
        context['collection_list'] = collection
        if collection.exists():
            collection = collection[0]
            if collection.UID_id == uid:
                if collection.books.filter(ISBN=book.ISBN).exists():
                    messages.info(request, "Books already in your collection")
                    return redirect("home")
                else:
                    collection.books.add(book)
                    messages.info(request,"This book add in your collection")
                    return redirect("collection", collection.id)
            else:
                return redirect("home")

def books_list_view(request):
    '''
    displays all books available in a orderly fashion
    for registered users
    '''
    context = {}
    books = Books.objects.all()
    user = request.user
    paginate_num = 20
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
    if user.is_authenticated:
        uid = Account.objects.get(username=user.username).id
        collections = Collection.objects.filter(UID=uid)
        context['collections'] = collections
        context['books'] = books
        context['uid'] = uid
        context['page_range'] = page_range
        context['max_index'] = max_index
        return  render(request, "books/books_list.html",context)
    else:
        context['page_range'] = page_range
        return redirect("home")



