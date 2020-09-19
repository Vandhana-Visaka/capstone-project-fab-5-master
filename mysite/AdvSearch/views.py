from django.shortcuts import render, redirect
from books.models import Books
from account.models import Account
from usercollections.models import Collection
from review.models import Review
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q, Count, Avg, F
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging

logger = logging.getLogger("django")
book_paginate_num = 12
user_paginate_num = 12
collection_paginate_num = 12
review_paginate_num = 12

@csrf_exempt
def adv_search_book(request):
    '''
    Allows user to search books using certain filters
    filters include genres, rating, 
    '''
    context = {}
    user = request.user
    title = request.GET.get("title") if request.GET.get("title") != None else ""
    isbn = request.GET.get("isbn") if request.GET.get("isbn") != None else ""
    genre = request.GET.get("genre") if request.GET.get("genre") != None else ""
    author = request.GET.get("author") if request.GET.get("author") != None else ""
    publisher = request.GET.get("publisher") if request.GET.get("publisher") != None else ""
    language = request.GET.get("language") if request.GET.get("language") != None else ""
    country = request.GET.get("country") if request.GET.get("country") != None else ""
    ratingUpper = request.GET.get("ratingUpper") if request.GET.get("ratingUpper") != None else ""
    ratingLower = request.GET.get("ratingLower") if request.GET.get("ratingLower") != None else ""
    logger.info(title)

    try:
        books_list = Books.objects.filter(
            Q(title__icontains=title) & Q(ISBN__icontains=isbn) & Q(genres__icontains=genre) & Q(publisher__icontains=publisher) & Q(language__icontains=language) & Q(authors__icontains=author) & Q(country__icontains=country)
        )
        reviews = Review.objects.filter(BID__in=books_list)
        rating = reviews.values('BID').annotate(avg_rating=Avg('rating'))
        if ratingLower != '':
            ratingLower = float(ratingLower)
            rating = rating.filter(Q(avg_rating__gte=ratingLower))
            books_list = books_list.filter(ISBN__in=rating.values('BID'))
        if ratingUpper != '':
            ratingUpper = float(ratingUpper)
            rating = rating.filter(Q(avg_rating__lte=ratingUpper))
            books_list = books_list.filter(ISBN__in=rating.values('BID'))

        paginator = Paginator(books_list, book_paginate_num)
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
        context['page_range'] = page_range
        context['max_index'] = max_index
        context['books_list'] = books_list
        
        if user.is_authenticated:
            context['uid'] = user.id
            collections = Collection.objects.filter(UID=user.id)
            context['collections'] = collections

        _mutable = request.GET._mutable
        request.GET._mutable = True
        if 'page' in request.GET:
            request.GET.pop('page')
        request.GET._mutable = _mutable

        return render(request, 'books/search_results.html', context)

    except Exception as e:
        logger.info(e)
        result_data = {
        	"error": True,
            "errorMessage": "Cannot search books!"
        }
        return JsonResponse(result_data, safe=False)

@csrf_exempt
def adv_search_user(request):
    '''
    Allows users to search similar or all users
    '''
    context = {}
    user = request.user
    username = request.GET.get("username") if request.GET.get("username") != None else ""

    if not user.is_authenticated:
        return redirect('home')
    context['uid'] = user.id

    try:
        user_list = Account.objects.filter(
            Q(username__icontains=username)
        )
        paginator = Paginator(user_list, user_paginate_num)
        page = request.GET.get('page',1)
        try:
            user_list = paginator.page(page)
        except PageNotAnInteger:
            user_list = paginator.page(1)
        except EmptyPage:
            user_list = paginator.page(paginator.num_pages)
        index = user_list.number-1
        max_index = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index else max_index
        page_range = list(paginator.page_range)[start_index:end_index]
        context['page_range'] = page_range
        context['max_index'] = max_index
        context['user_list'] = user_list

        _mutable = request.GET._mutable
        request.GET._mutable = True
        if 'page' in request.GET:
            request.GET.pop('page')
        request.GET._mutable = _mutable

        return render(request, 'books/search_results.html', context)

    except Exception as e:
        logger.info(e)
        result_data = {
            "error": True,
            "errorMessage": "Cannot search users!"
        }
        return JsonResponse(result_data, safe=False)


@csrf_exempt
def adv_search_collection(request):
    '''
    allows users to search collections
    allows users to access other collections
    '''
    context = {}
    user = request.user
    collectionName = request.GET.get("collectionName") if request.GET.get("collectionName") != None else ""
    lowerBound = request.GET.get("lowerBound") if request.GET.get("lowerBound") != None else ""
    upperBound = request.GET.get("upperBound") if request.GET.get("upperBound") != None else ""

    if not user.is_authenticated:
        return redirect('home')
    context['uid'] = user.id

    try:
        collection_list = Collection.objects.filter(
            Q(collectionName__icontains=collectionName)
        )

        logger.info(lowerBound)
        if lowerBound != '':
            lowerBound = int(lowerBound)
            print(lowerBound)
            collection_list = collection_list.annotate(c=Count('books')).filter(c__gt=lowerBound)
        if upperBound != '':
            upperBound = int(upperBound)
            collection_list = collection_list.annotate(c=Count('books')).filter(c__lt=upperBound)

        paginator = Paginator(collection_list, collection_paginate_num)
        page = request.GET.get('page',1)
        try:
            collection_list = paginator.page(page)
        except PageNotAnInteger:
            collection_list = paginator.page(1)
        except EmptyPage:
            collection_list = paginator.page(paginator.num_pages)
        index = collection_list.number-1
        max_index = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index else max_index
        page_range = list(paginator.page_range)[start_index:end_index]
        context['page_range'] = page_range
        context['max_index'] = max_index
        context['collection_list'] = collection_list

        _mutable = request.GET._mutable
        request.GET._mutable = True
        if 'page' in request.GET:
            request.GET.pop('page')
        request.GET._mutable = _mutable

        return render(request, 'books/search_results.html', context)

    except Exception as e:
        logger.info(e)
        result_data = {
            "error": True,
            "errorMessage": "Cannot search collections!"
        }
        return JsonResponse(result_data, safe=False)


@csrf_exempt
def adv_search_review(request):
    '''
    allows users to search reviews and view reviews and ratings
    '''
    context = {}
    user = request.user
    username = request.GET.get("username") if request.GET.get("username") != None else ""
    title = request.GET.get("title") if request.GET.get("title") != None else ""

    if not user.is_authenticated:
        return redirect('home')
    context['uid'] = user.id

    try:
        logger.info(title)
        review_list = Review.objects.filter(UID__in=Account.objects.filter(Q(username__icontains=username)))
        review_list = review_list.filter(BID__in=Books.objects.filter(Q(title__icontains=title)))

        paginator = Paginator(review_list, review_paginate_num)
        page = request.GET.get('page',1)
        try:
            review_list = paginator.page(page)
        except PageNotAnInteger:
            review_list = paginator.page(1)
        except EmptyPage:
            review_list = paginator.page(paginator.num_pages)
        index = review_list.number-1
        max_index = len(paginator.page_range)
        start_index = index - 3 if index >= 3 else 0
        end_index = index + 3 if index <= max_index else max_index
        page_range = list(paginator.page_range)[start_index:end_index]
        context['page_range'] = page_range
        context['max_index'] = max_index
        context['review_list'] = review_list

        _mutable = request.GET._mutable
        request.GET._mutable = True
        if 'page' in request.GET:
            request.GET.pop('page')
        request.GET._mutable = _mutable

        return render(request, 'books/search_results.html', context)

    except Exception as e:
        logger.info(e)
        result_data = {
            "error": True,
            "errorMessage": "Cannot search collections!"
        }
        return JsonResponse(result_data, safe=False)
