from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from account.models import Account
from datetime import datetime
from .forms import AddGoalForm
from .models import Goal
from books.models import Books
from django.contrib import messages
import json

def goal_view(request):
    '''
    allows users to view the number of books to read as goal
    '''
    context={}
    user = request.user
    if user.is_authenticated:
        uid = Account.objects.get(username=user.username)
        if request.method == 'POST':
            numBooks = request.POST.get('numBooks')
            goal = Goal(UID=uid,numBooks=numBooks)
            goal.save()
            return redirect('user_homepage')
        return render(request, 'personal/user_homepage.html', context)

def goal_detail_view(request):
    '''
    allows users to view goal and the progress made so far
    '''
    context = {}
    user = request.user
    current_year = datetime.now().year
    current_month = datetime.now().month
    context['hide'] = False
    if user.is_authenticated:
        uid = Account.objects.get(username=user.username)
        goal = Goal.objects.filter(UID=uid,year=current_year,month=current_month)
        if goal.exists():
            goal = goal[0]
            books = goal.books.all()
            context['goal'] = goal
            context['hide'] = True
            context['books'] = books
            if goal.numBooks == 0:
                context['percentage'] = 0
            else:
                context['percentage'] = round(goal.numFinished / goal.numBooks)
    return render(request,'goal_detail.html',context)

@csrf_exempt
def edit_goal_view(request):
    '''
    updating goal according to the read or currently reading
    '''
    data = request.POST.get('data')
    if data != None:
        data = json.loads(data)
    user = request.user
    if user.is_authenticated:
        uid = Account.objects.get(username=user.username)
        try:
            goal=Goal.objects.get(UID=uid,year=data['year'],month=data['month'])
            goal.numBooks = data['numBooks']
            goal.save()
            return_data={"error":False,"errorMessage":"Updated Successfully"}
            return JsonResponse(return_data, safe=False)
        except:
            return_data={"error":True,"errorMessage":"Failed to Update Data"}
            return JsonResponse(return_data, safe=False)

@csrf_exempt
def goal_delete_view(request):
    '''
    reset or change the goal or change it to zero
    '''
    data = request.POST.get('data')
    if data != None:
        data = json.loads(data)
    user = request.user
    if user.is_authenticated:
        uid = Account.objects.get(username=user.username)
        try:
            goal=Goal.objects.get(UID=uid,year=data['year'],month=data['month'])
            goal.delete()
            return_data={"error":False,"errorMessage":"Deleted Successfully"}
            return JsonResponse(return_data,safe=False)
        except:
            return_data={"error":True,"errorMessage":"Failed to Delete Data"}
            return JsonResponse(return_data,safe=False)


def record_books_read(request, book_id):
    '''
    record all books that have been read or added to collection to update the user goal
    '''
    book = get_object_or_404(Books, ISBN=book_id)
    user = request.user
    current_year = datetime.now().year
    current_month = datetime.now().month
    if user.is_authenticated:
        uid = Account.objects.get(username=user.username).id
        goal = Goal.objects.filter(UID=uid,year=current_year,month=current_month)
        if goal.exists():
            goal = goal[0]
            if goal.books.filter(ISBN=book.ISBN).exists():
                messages.info(request, "Books already in your collection")
                return redirect("collections")
            else:
                goal.numFinished += 1
                goal.books.add(book)
                goal.save()
                messages.info(request,"This book add in your collection")
                return redirect("collections")
            
