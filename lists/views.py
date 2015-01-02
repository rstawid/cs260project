from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
from django.contrib.auth import authenticate, login, logout
#to restrict access using decorators
from django.contrib.auth.decorators import login_required
from lists.forms import UserForm
from django.utils import timezone
from django.contrib.auth.models import User
from django import forms


def view_user_list(request, username):
	if request.user.is_active and request.user.is_authenticated():
		if request.user.username == username: 
			item_ = Item.objects.filter(list__name=username)
			return render(request, 'list.html', {'list': item_, 'currentdate':timezone.now()})
		else:
			return HttpResponse("You don't have access to this page.")
	else:
		return redirect ('/')

def add_item(request, username):
	if request.user.is_active and request.user.username == username:
		if request.method == 'POST':
			list_ = List.objects.get(name=username)
			Item.objects.create(text=request.POST['item_text'], list=list_)
			return redirect('/lists/%s/' % (username,))
		else:
			return redirect ('/lists/%s/' % (username,)) 
	else:
		return redirect('/')

def change_item(request, username):
	if request.user.is_active and request.user.username == username:
		if request.method == 'POST':
			itemID = request.POST['item_id']
			done = request.POST['done']
			item = Item.objects.get(id=itemID)
			item.done=int(done)
			item.done_date = timezone.now()
			item.save()
			return redirect ('/lists/%s/' % (username,)) 
		else:
			return redirect ('/lists/%s/' % (username,)) 
	else:
		return redirect('/')

	
def user_login(request):
	if request.method == 'POST':
		username = request.POST['username']
		password = request.POST['password']
		
		user = authenticate(username=username, password=password)
		
		if user:
			if user.is_active:
				login(request, user)
				list_ = List.objects.get_or_create(name=user.username)
				return redirect ('/lists/%s/' % (username,)) 
			else:
				return HttpResponse("Your account is disabled")
		else:
			loginfailed = True
			return render(request, 'login.html', {'loginfailed': loginfailed})
#			return HttpResponse("Invalid login details supplied. Go back and log-in again.")
			
	else:
		return render(request, 'login.html', {})

'''		
def register(request):
	registered = False
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			new_user = form.save()
			registered = True
	else:
		form = UserCreationForm()
		return render(request, 'register.html', {'form': form, 'registered': registered})
	return render(request, 'register.html', {'registered': registered})
'''	
@login_required
def user_logout(request):
	#since user is logged-in, just log them out
	logout(request)
	
	#take the user back to homepage
	return redirect('/lists/login/')

def register(request):
	registered = False
	if request.method == 'POST':
		form = UserForm(request.POST)
		if form.is_valid():
			user = form.save()
			user.set_password(user.password)
			user.save()
			registered = True

	else:
		form = UserForm()
	
	return render(request, 'register.html', {
        'form': form, 'registered': registered}
		)
	