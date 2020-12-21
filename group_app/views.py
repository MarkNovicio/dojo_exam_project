from django.shortcuts import render, redirect
from django.contrib import messages
from login_app.models import *
from group_app.models import *
from .models import *
from django.db.models import Count
import bcrypt


def groups_index(request):
    if 'user_id' in request.session:
        context = {
            "groups": Group.objects.annotate(Count('join')).order_by('-join__count'),
            #"groups": Group.objects.all(),
            "user": Registration.objects.get(id = request.session['user_id'])
        }
        return render(request, "groups.html", context)

    else:    
    
        return redirect('/')

def create_group(request):
    errors = Group.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        print(errors)
        return redirect('/groups')

    else:
        user = Registration.objects.get(id=request.session['user_id'])
        group = Group.objects.create(
            org_name = request.POST['org_name'],
            description = request.POST['description'],
            publisher = Registration.objects.get(id = request.session['user_id'])
        )

        user.joined.add(group)

        return redirect('/groups')

def show_group(request, group_id):
    if 'user_id' in request.session:

        context = {
            "group": Group.objects.get(id=group_id),
            "user": Registration.objects.get(id = request.session['user_id'])
        }
        return render(request, "group_profile.html", context)
    else:    
        return redirect('/')

def join_group(request, group_id):
    join_group = Group.objects.get(id=group_id)
    user = Registration.objects.get(id=request.session['user_id'])

    join_group.join.add(user)

    return redirect(f'/groups/{group_id}')

def leave_group(request, group_id):
    leave_group = Group.objects.get(id=group_id)
    user = Registration.objects.get(id=request.session['user_id'])

    leave_group.join.remove(user)

    return redirect(f'/groups/{group_id}')

def delete_group(request, group_id):
    delete_group = Group.objects.get(id=group_id)
    if delete_group.publisher.id == request.session['user_id']:
        delete_group.delete()

    return redirect('/groups')

def logout(request):
    del request.session['user_id']
    return redirect('/')