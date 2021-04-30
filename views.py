from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.contrib.auth.models import User, auth
from django.contrib.auth import logout as original_logout
from django.urls import reverse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from .models import Blogs, profile, Review
from .forms import UserUpdateForm, ProfileUpdateForm, UploadForm, ReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, HttpResponseRedirect
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.generic import DetailView
from django.db.models import Avg
from django.http import JsonResponse
# Create your views here.

def index(request):
    blog = Blogs.objects.order_by('-created_date')
    p = Paginator(blog, 6)
    page_number = request.GET.get('page', 1)
    page = p.page(page_number)
    context ={"Foodie_Blogs": page}      
    return render(request, "index.html", context)


def login_page(request):
	return render(request, 'login.html')

def signup_page(request):
	return render(request, 'signup.html')

def signup(request):
	if request.method == 'POST':
		firstname = request.POST['firstname']
		lastname = request.POST['lastname']
		username = request.POST['username']
		gmail = request.POST['gmail']
		password = request.POST['password']

		if User.objects.filter(username= username).exists():
			messages.error(request, 'Sorry!!! Username is already taken')
			return redirect('/signup_page/')

		elif User.objects.filter(email= gmail).exists():
			messages.error(request, 'Sorry!!! The account from this email is already made!')
			return redirect('/signup_page/')

		else:
			user= User.objects.create_user(first_name = firstname, last_name = lastname,email= gmail, username = username, password= password)
			user.save()
			messages.info(request, 'Account created succesfully.')
			return redirect('/login_page/')
	else:
		return render(request, '/signup_page/')

@csrf_exempt
def login(request):
	if request.method == 'POST':
		login_username = request.POST['usernamelogin']
		login_password = request.POST['passwordlogin']

		user = auth.authenticate(username= login_username, password= login_password)
		
		if user is not None:
			auth.login(request, user)
			messages.success(request, 'User logged in.')
			return redirect('/')

		else:
			messages.error(request, 'Invalid username or password!! Try with correct one.')
			return redirect('/login_page/')

	else:
		return redirect('/login_page/')

def logout_view(request, *args, **kwargs):
    """
    Info on why this exists: http://code.djangoproject.com/ticket/6941
    Clears out any session data on logout that would otherwise persist
    for any subsequent logins regardless of user_id.
    """
    for sesskey in request.session.keys():
        del request.session[sesskey]
    return original_logout(request, *args, **kwargs)

"""
def logout_view(request):
    logout(request)
    messages.success(request,"Successfully logged out")
    return redirect("/")
"""
"""
def logout(request):
	auth.logout(request)
	messages.info(request, 'Successfully logged out !')
	return redirect('/')
"""

@login_required
def profile(request):
   if request.user.is_authenticated:
        user = request.user
        context ={} 
        context["Foodie_Blogs"] = Blogs.objects.filter(Author=request.user)
        user_posts = Blogs.objects.filter(Author=request.user).order_by('-created_date')
        return render(request, 'profile.html', {'Foodie_Blogs':user_posts,'user': user})
   else:
        return redirect('/login_page')


@login_required
def updateprofile(request):
        if request.method == 'POST':
            u_form = UserUpdateForm(request.POST, instance=request.user)
            p_form = ProfileUpdateForm(request.POST,
			                           request.FILES, instance=request.user.profile)
            if u_form.is_valid() and p_form.is_valid():
                u_form.save()
                p_form.save()
                messages.info(request, 'Successfully updated your profile!!!')
                return redirect('/profile')
        else:
            u_form = UserUpdateForm(instance=request.user)
            p_form = ProfileUpdateForm(instance=request.user.profile)
        context = {
			'u_form' : u_form,
			'p_form' : p_form
		}
        return render(request, 'updateprofile.html', context)
#def upload(request):
#	return render(request, 'view.html')

def passwordchange(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.info(request, 'Your password was successfully updated!')
            return redirect('/profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'password_change.html', {
        'form': form
    })

def passwordresetdone(request):
	return render(request, 'password_change_done.html')

@login_required
def create_post(request): 
    form = UploadForm()
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.Author=request.user
            instance.save()
            messages.success(request, 'Successfully posted your blog!!!')
            return redirect('/profile')
	
    context ={'form': form} 
    return render(request, "view.html", context)
	

def list_post(request): 
    posts = Blogs.objects.all()
    paginator = Paginator(posts, 1) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'index.html', {'page_obj': page_obj})
 
def detail_post(request, pk): 
    data = Blogs.objects.get(id = pk) 
    reviews = Review.objects.filter(blog = pk).order_by('-pub_date')
    average = reviews.aggregate(Avg("rating"))["rating__avg"]
    if average == None:
        average = 0
    average = round(average, 2)
    context={
        "data" : data,
        "reviews" : reviews,
        "average": average
    }
    return render(request, "detailpost.html", context) 

@login_required
def addreview(request, pk):
    data = Blogs.objects.get(id = pk)
    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():    
            review = form.save(commit=False)
            review.comment = request.POST["comment"]
            review.rating = request.POST["rating"]
            review.user = request.user
            review.blog = data
            review.save()
            #return render(request, 'detailpost.html')
            return redirect("detail_post", pk)      
    else:
        form = ReviewForm()
    context={'data' : data, 'form': form}
    return render(request, 'detailpost.html', context)



def Rate(request, pk):
    Blogs = Blogs.objects.get(id=pk)
    form = ReviewForm()

    if request.method == "POST":
        form = ReviewForm(request.POST)
        if form.is_valid():
            data = form.save(commit=False)
            data.user = request.user
            data.Blogs = Blogs
            data.save()
            return redirect("detailpost.html")
    else:
        form = ReviewForm()
    context = {"form": form}
    return render(request, "detailpost.html", context)

@login_required
def update_post(request, pk): 
    posts = Blogs.objects.get(id=pk) 
    form = UploadForm(instance = posts) 
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES, instance = posts) 
        if form.is_valid(): 
            form.save() 
            messages.info(request, 'Successfully updated your blog!!!')
            return redirect('/profile')
    return render(request, "updatepost.html", { 'form' : form, 'posts': posts})
		
# delete view for details 
@login_required
def delete_post(request, pk): 
    context ={} 
  
    # fetch the object related to passed id 
    obj = get_object_or_404(Blogs, id = pk) 
  
  
    if request.method =="POST": 
        # delete object 
        obj.delete() 
        # after deleting redirect to  
        # home page 
        return HttpResponseRedirect("/") 
  
    return render(request, "deleteview.html", context) 

def search(request):
    blog = Blogs.objects.all().order_by('-created_date')
    query = request.GET['query']
    if query:
       blog = Blogs.objects.filter(
	        Q(title__icontains=query) | 
	        Q(ingredients__icontains=query)).distinct()
    paginator = Paginator(blog, 2)
    page_number = request.GET.get('page')

    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    context ={"Foodie_Blogs": page} 
    return render(request, "search.html", context)
    return HttpResponse('This is search')

import numpy as np
import pandas as pd
import scipy as sp
import pymysql

import sqlalchemy
from . import Recommendation
import pickle
engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost:3306/Foodie')
food = pd.read_sql_table('foodie_blogs',engine)
Reviews = pd.read_sql_table('foodie_review',engine)
Data = pd.merge(Reviews, food)

def anything(request):
    if request.user.is_authenticated:
        blog = Blogs.objects.all()
        rec=Blogs.objects.get(Recommendation.Recommendations(blog.title).array[0])
        return render(request, Related.html, {'rec': rec})


#yo try gareko arko Recommendation ho
def related(request,blog_id=-1):
	new_obj = return_related_food(blog_id)
	
	return render(request, 'Related.html', {"blogs":new_obj})

def return_related_food(blog_id):
	with open("modelfile.pickle","rb") as f:
		cosine_sim = pickle.load(f)
	new_obj = Data
	food_list = []
	index_list = []
	for index,blog in enumerate(new_obj):
		food_list.append(blog_id)
		index_list.append(index)

	indices = pd.Series(index_list,index=food_list)
	print(indices.head(n=20))
	idx = indices[blog_id]
	scores = list(enumerate(cosine_sim[index]))
	similarity_scores = sorted(scores, key=lambda x: x[1], reverse=True)
	similarity_scores = similarity_scores[:4]
	match_index = [i[0] for i in similarity_scores]
	print(match_index)
	blogs = []
	for index,blog in enumerate(new_obj):
		if index in match_index:
			blogs.append(blog)

	return blogs
	print(blogs)