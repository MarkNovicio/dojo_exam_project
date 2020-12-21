from django.shortcuts import render, redirect
from django.contrib import messages
import bcrypt
from .models import *

def index(request):

    return render(request, "index.html")

def create_registration(request):
    if request.method == 'GET':
        return redirect('/')
    errors = Registration.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/')
    
    else:
        pw_hash = bcrypt.hashpw(request.POST['password'].
        encode(), bcrypt.gensalt(rounds =13)).decode()
        new_user = Registration.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw_hash
        )

        request.session['user_id'] = new_user.id
        request.session['first_name']= new_user.first_name
        request.session['last_name']= new_user.last_name
        request.session['email']= new_user.email
        # context = {
        #     "new_user_added": Registration.objects.get(id=request.session['user_id'])
        # }
        #i need to redirect not render
        return redirect('/')

def login(request):
    if request.method == "GET":
        return redirect('/')
    if not Registration.objects.authenticate(request.POST['email'], request.POST['password']):
        messages.error(request, 'Invalid email/password')
        return redirect('/')
    else:
        logged_users = Registration.objects.filter(email=request.POST['email'])
        user = logged_users[0]
        request.session['user_id'] = user.id
        request.session['first_name']= user.first_name
        request.session['last_name']=user.last_name
        request.session['email']= user.email

        #return render(request, "message_wall.html", context)
        return redirect('/groups') #change this redirect to the page you want to redirect

def logout(request):
    del request.session['user_id']
    del request.session['first_name']
    del request.session['last_name']
    del request.session['email']

    #request.session.clear()
    return redirect('/')

    