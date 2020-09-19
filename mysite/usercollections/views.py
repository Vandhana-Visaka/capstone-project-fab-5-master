from django.shortcuts import render, redirect
from usercollections.models import Collection, Booksadd
from account.models import Account
from books.models import Books
from goals.models import Goal
from usercollections.forms import CreateACollectionForm, AddBookISBNForm
from django.http import Http404, HttpResponse, HttpResponseRedirect
import json
from datetime import datetime
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import logging
logger = logging.getLogger("django")

# include create collection and the list of collection names
def collections_view(request):
    '''
    Displays Collections of a User
    Preset collections include read, currently reading and want to read
    Named collection can be created
    '''
    context = {}
    user = request.user
    current_year = datetime.now().year
    current_month = datetime.now().month
    context['goalShow'] = False
    if user.is_authenticated:
        uid = Account.objects.get(username=user.username).id
        goal = Goal.objects.filter(UID=uid,year=current_year,month=current_month)
        if goal.exists():
            if goal[0].numFinished == goal[0].numBooks:
                context['goalShow'] = True
        collections = Collection.objects.filter(UID=uid)
        context['uid'] = uid
        context['collections'] = collections
        context['update_forbid'] = ["Read","Want to Read","Currently Reading"]
    else:
        return redirect('home')

    return render(request, 'collections.html', context)

@csrf_exempt
def collection_add(request):
    '''
    Allows user to add a collection - named collection and provide description
    '''
    context = {}
    user = request.user
    if user.is_authenticated:
        collectionName = request.POST.get("collectionName")
        description = request.POST.get("description")

        try:
            if Collection.objects.filter(UID=user, collectionName=collectionName):
                collection_data = {
                    "error": True,
                    "errorMessage": "Duplicated collection"
                }
            else:
                collection = Collection(UID=user, collectionName=collectionName, description=description)
                collection.save()
                collection_data = {
                    "id": collection.id,
                    "created_at": collection.createdDate,
                    "error": False,
                    "errorMessage": "Add a collection successfully"
                }
            return JsonResponse(collection_data, safe=False)
        except Exception as e:
            collection_data = {
                "error": True,
                "errorMessage": "Cannot add a collection"
            }
            return JsonResponse(collection_data, safe=False)



def collection_view(request, collection_id):
    '''
    Add book to collection and the list of books in collection
    '''
    context = {}
    paginate_num = 20
    user = request.user
    current_year = datetime.now().year
    current_month = datetime.now().month
    context['hide'] = False
    if user.is_authenticated:
        uid = Account.objects.get(username=user.username).id
        context['uid'] = uid
        context['collection_id'] = collection_id
        collection = Collection.objects.get(pk=collection_id)
        goal = Goal.objects.filter(UID=uid,year=current_year,month=current_month)
        if goal.exists():
            context['hide'] = True
        context['UID_id'] = collection.UID_id
        books_list = collection.books.all()
        context['books_list'] = books_list
        context['books_id'] = json.dumps([int(book.ISBN) for book in context['books_list']])
        context['collectionName'] = collection.__str__()
        
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

        context['books_list'] = books_list
        context['page_range'] = page_range
        context['max_index'] = max_index
        context['collectionUserName'] = collection.UID.username

        if request.POST:

            if collection.UID_id == uid:

                form = AddBookISBNForm(request.POST)

                try:
                    book = Books.objects.get(ISBN=request.POST['ISBN'])
                    if collection.books.filter(ISBN=request.POST['ISBN']).exists():
                        context['add_book_ack'] = 'This book {} has been added already'.format(request.POST['ISBN'])
                        context['addBookISBNForm'] = AddBookISBNForm()
                    else:
                        collection.books.add(book)
                        collection.save()
                        return redirect('collection', collection_id)
                except Books.DoesNotExist:
                    context['addBookISBNForm'] = AddBookISBNForm()
                    context['add_book_ack'] = 'This book does not exist'

            else:
                return redirect('collection', collection_id)

        else:
            form = AddBookISBNForm()
            context['addBookISBNForm'] = form

    else:
        return redirect('home')

    return render(request, 'collection.html', context)


def book_delete(request, collection_id, book_id):
    '''
    User can delete a book from collection
    '''
    context = {}
    user = request.user

    if user.is_authenticated:
        uid = Account.objects.get(username=user.username).id
        context['collection_id'] = collection_id
        collection = Collection.objects.get(pk=collection_id)
        
        if collection.UID_id == uid:
        
            book = Books.objects.get(pk=book_id)
            collection.books.remove(book)
            collection.save()
            return redirect('collection', collection_id)
        else:
            return redirect('collection', collection_id)
    return render(request, 'collection.html', context)


@csrf_exempt
def collection_delete(request):
    '''
    User can delete a collection as a whole
    The books in the collection is also deleted from the collection
    '''
    id = request.POST.get('id')
    try:
        collection=Collection.objects.get(id=id)
        collection.delete()
        collection_data={"error":False,"errorMessage":"Deleted Successfully"}
        return JsonResponse(collection_data,safe=False)
    except:
        collection_data={"error":True,"errorMessage":"Failed to Delete Data"}
        return JsonResponse(collection_data,safe=False)

@csrf_exempt
def collection_update(request):
    '''
    Collections can be updated when books are added or deleted 
    '''
    data = request.POST.get('data')
    data = json.loads(data)
    try:
        collection=Collection.objects.get(id=data['id'])
        if collection.collectionName != data['collectionName'].strip() and Collection.objects.filter(UID=request.user, collectionName=data['collectionName'].strip()):
            return_data = {
                "error": True,
                "errorMessage": "Duplicated collection",
                "collectionName": collection.collectionName,
                "collectionID": collection.id
            }
        else:
            collection.collectionName = data['collectionName'].strip()
            collection.description = data['description'].strip()
            collection.save()
            return_data={"error":False,"errorMessage":"Updated Successfully"}
        return JsonResponse(return_data, safe=False)
    except:
        return_data={"error":True,"errorMessage":"Failed to Update Data"}
        return JsonResponse(return_data, safe=False)


def recentAdd_view(request):
    '''
    Allows users to access recently added books and allows other users to do the same
    Can view recently added - 5,10,15
    '''
    if request.is_ajax():
        num = int(request.GET['num'])
        collection_id = request.GET['collection_id']
        collection = Collection.objects.get(pk=collection_id)
        booksadd = [a for a in collection.booksadd_set.all()]
        if num != 0:
            sortedbooks = sorted(booksadd,key=lambda x: x.added_at,reverse=True)[:num]
        else:
            sortedbooks = sorted(booksadd,key=lambda x: x.added_at,reverse=True)
        json_list = []
        for b in sortedbooks:
            book = Books.objects.get(pk=b.book)
            j = {
                "cover": str(book.cover),
                "ISBN": book.ISBN,
                "title":book.title,
                "authors":book.authors,
                "genres":book.genres,
                "language":book.language,
                "country":book.country,
                "num_page":book.num_page,
                "publication_date":str(book.publication_date),
                "publisher":book.publisher,
            }
            json_list.append(j)
        return HttpResponse(json.dumps(json_list),content_type ='application/json')
    else:
        raise Http404

@csrf_exempt
def add_book_to_collection(request):
    '''
    Allows users to add a book to a collection if the collection exists
    Can be done through ISBN form
    Or through add to collection button on book page and home page
    '''
    user = request.user
    if user.is_authenticated:
        isbn = request.POST.get("isbn")
        collection_id = request.POST.get("collection_id")
        try:
            book = Books.objects.get(ISBN=isbn)
            collection = Collection.objects.get(pk=collection_id)
            collection.books.add(book)
            collection.save()
            add_book_data = {
                "isbn": book.ISBN,
                "collection_id": collection.id,
                "error": False,
                "errorMessage": "Add a book to the collection successfully!"
            }
            return JsonResponse(add_book_data, safe=False)
        
        except Exception as e:
            logger.info(e)
            add_book_data = {
                "error": True,
                "errorMessage": "Cannot add a book"
            }
            return JsonResponse(add_book_data, safe=False)
