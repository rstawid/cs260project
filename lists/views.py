from django.shortcuts import redirect, render
from django.http import HttpResponse
from lists.models import Item, List
from django.contrib.auth import authenticate, login, logout
#to restrict access using decorators
from django.contrib.auth.decorators import login_required
import datetime

# Create your views here.
def home_page(request):
	return render(request, 'home.html')

def view_list(request, list_id):
	list_ = List.objects.get(id=list_id)
	now = datetime.datetime.now()
	today = now.strftime("%A, %b %d, %Y")
	return render(request, 'list.html', {'list': list_, 'currentdate':today})

def new_list(request):
	list_=List.objects.create()
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%d/' % (list_.id,)) 

def add_item(request, username):
	list_ = List.objects.get(name=username)
	Item.objects.create(text=request.POST['item_text'], list=list_)
	return redirect('/lists/%s/' % (list_.name,)) 
	
@login_required
def view_user_list(request, username):
	now = datetime.datetime.now()
	list_ = List.objects.get(name=username)
	today = now.strftime("%A, %b %d, %Y")
	return render(request, 'list.html', {'list': list_, 'currentdate':today})
	
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
			return HttpResponse("Invalid login details supplied.")
			
	else:
		return render(request, 'login.html', {})
@login_required
def user_logout(request):
	#since user is logged-in, just log them out
	logout(request)
	
	#take the user back to homepage
	return redirect('/lists/login/')
	
def change_item(request, username):
	if request.method == 'POST':
		itemID = request.POST['item_id']
		done = request.POST['done']
		done2 = int(done)
#		list_ = Item.objects.all()
		omeng = Item.objects.get(id=itemID)
		omeng.done=done2
		omeng.save()
#		return HttpResponse("SUCCESSFULL! Change status of item: " + omeng.text + " Status: " + done)
		return redirect ('/lists/%s/' % (username,)) 
#		for item in list_.item_set.all():
#		for item in list_:
#			if item.id == itemID:
#				item.done = done2
#				item.save()
#				return HttpResponse("SUCCESSFULL! Change status of item: " + item.text + " Status: " + done2)
#			else: return HttpResponse("NO ENTRY!!!: Change status of item: " + itemID + " Status: " + done)
#		return redirect ('/lists/%s/' % (username,)) 
	else:
		return redirect("/")