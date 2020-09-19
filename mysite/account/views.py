from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate,logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from books.models import Books
from .models import Account
from usercollections.models import Collection
import datetime
import numpy as np
from sklearn.neighbors import NearestNeighbors
import sklearn

def similar_users(request):
    '''
    allows users to find similar users
    '''
    user = request.user
    dic = {'Male': 0, 'Female': 1, 'Other': 2}
    usernames = []
    data = []
    for account in Account.objects.all():
        usernames.append(account.username)
        data.append([(datetime.date.today()-account.birthday).days, dic[account.gender]])
    if len(usernames) <= 5:
        for i in usernames:
            tmp_user = Account.objects.get(username=i)
            tmp = ''
            for j in usernames:
                if i != j:
                    tmp = tmp + j + '/'
            tmp_user.similar_users = tmp
            tmp_user.save()
    else:
        X = np.array(data)
        X = sklearn.preprocessing.scale(X)
        nbrs = NearestNeighbors(n_neighbors=5, algorithm='ball_tree').fit(X)
        distance, indices = nbrs.kneighbors(X)
        for u in range(len(indices)):
            tmp_user = Account.objects.get(username=usernames[u])
            tmp = ''
            for s in indices[u]:
                if s != u:
                    tmp = tmp + usernames[s] + '/'
            tmp_user.similar_users = tmp
            tmp_user.save()


def registration_view(request):
    ''' 
    allows user to register using the registration form
    details are updated as account object
    '''
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            if '/' in form.cleaned_data.get('username'):
                context['registration_form'] = form
                form.add_error('username','invalid punctuation in username')
            else:
                form.save()
                email = form.cleaned_data.get('email')
                raw_password = form.cleaned_data.get('password1')
                account = authenticate(email=email,password=raw_password)
                username = form.cleaned_data.get('username')
                uid = Account.objects.get(username=username)
                read = Collection(UID=uid, collectionName='Read', description='Read')
                want_to_read = Collection(UID=uid, collectionName='Want to Read', description='Want to Read')
                currently_reading = Collection(UID=uid, collectionName='Currently Reading', description='Currently Reading')
                read.save()
                want_to_read.save()
                currently_reading.save()
                if len(Account.objects.all()) > 1:
                    similar_users(request)
                login(request,account)
                return redirect('home')
        else:
            context['registration_form'] = form
            context['register_email'] = request.POST['email']
            context['register_username'] = request.POST['username']
            context['register_firstname'] = request.POST['firstname']
            context['register_lastname'] = request.POST['lastname']
            context['register_birthday'] = request.POST['birthday']
            if request.POST['gender'] == 'Male':
                context['male_checked'] = 'checked'
            elif request.POST['gender'] == 'Female':
                context['female_checked'] = 'checked'
            elif request.POST['gender'] == 'Other':
                context['other_checked'] = 'checked'
            render(request, 'account/register.html',context)
    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return  render(request, 'account/register.html',context)


def logout_view(request):
    logout(request)
    return redirect('home')

def login_view(request):
    '''
    Shows the user email and password
    Allows user to reset password
    '''
    context = {}
    user = request.user
    if user.is_authenticated:
        return redirect("home")
    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email,password=password)

            if user:
                login(request, user)
                return redirect("home")
    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form
    return render(request, 'account/login.html',context)

def account_view(request):
    '''
    allows user to view account details if authenticated
    '''
    if not request.user.is_authenticated:
        return redirect('login')

    context = {}
    user = request.user
    context['uid'] = user.id

    if request.POST:
        form = AccountUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            if '/' in request.POST['username']:
                form.add_error('username', 'invalid punctuation in username')
            else:
                form.initial = {
                    "email": request.POST['email'],
                    "username": request.POST['username'],
                }
                form.save()
                context['success_message'] = "Updated"
    else:
        form = AccountUpdateForm(
            initial = {
                "email": request.user.email,
                "username": request.user.username,
            }
        )
    context['account_form'] = form
    return render(request, 'account/account.html',context)
