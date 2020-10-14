from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404
from django.core.paginator import Paginator
from django.contrib.auth import authenticate
from django.contrib import messages
import requests
import bcrypt
from .models import Movie, User
from django.contrib import admin, auth

# Create your views here.
url = "http://omdbapi.com/?apikey="
api_key = "a6875c33"


def index(request):
    user = User.objects.get(id=request.session['user_id'])
    return render(request, 'index.html', {'user': user})


def result(request):
    movie_title = request.POST["one"]
    params = {
        "s": movie_title
    }
    response = requests.get(url + api_key, params=params)
    print(response.json())
    if (response.json()['Response'] == "False"):
        return render(request, 'test.html')
    else:
        movies = response.json()["Search"]
        return render(request, 'result.html', {'movies': movies})


def movieDetail(request):
    movie_detail = request.GET["movie_title"]
    params = {
        "t": movie_detail
    }
    response = requests.get(url + api_key, params=params)
    movie = response.json()
    return render(request, 'detail.html', {'movie': movie})


def dashboard(request):
    user = User.objects.get(id=request.session['user_id'])
    # movies = Movie.objects.filter(users=user).order_by("-created_at")
    movies = user.movies.all().order_by("-created_at")
    paginator = Paginator(movies, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'movies': user.movies.all(),
        'page_obj': page_obj,
        'user': user
    }

    return render(request, 'list.html', context)


def add_movie(request):
    user = User.objects.get(id=request.session['user_id'])
    movie_detail = request.POST["movie_title"]
    params = {
        "t": movie_detail
    }
    response = requests.get(url + api_key, params=params)
    movie = response.json()
    created_movie = Movie.objects.create(
        title=movie['Title'], genre=movie['Genre'], run_time=movie['Runtime'], poster=movie['Poster'])
    user.movies.add(created_movie)
    return redirect('/dashboard')


def delete_movie(request, movie_id):
    user = User.objects.get(id=request.session['user_id'])
    deleted_movie = Movie.objects.get(id=movie_id)
    deleted_movie.delete()
    return redirect('/dashboard')


def edit_movie(request, movie_id):
    user = User.objects.get(id=request.session['user_id'])
    movie = Movie.objects.get(id=movie_id)
    return render(request, 'edit.html', {'movie': movie})


def update_movie(request, movie_id):
    user = User.objects.get(id=request.session['user_id'])
    updated_movie = Movie.objects.get(id=movie_id)
    updated_movie.title = request.POST['title']
    updated_movie.genre = request.POST['genre']
    updated_movie.save()
    return redirect('/dashboard')
# -------------------------------------------------------------------------------------------------------------------------------------------------------


def log(request):
    return render(request, 'log.html')


def register(request):
    password = request.POST['password']
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    errors = User.objects.basic_validator(request.POST)
    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'],
                                   email=request.POST['email'],  password=pw_hash, confirm_password=request.POST['confirm_password'])
        request.session['first_name'] = user.first_name
        request.session['user_id'] = user.id

        return redirect('/index')


def login(request):
    errors = User.objects.login_validator(request.POST)
    print(errors)
    if (errors):
        for key, value in errors.items():
            messages.error(request, value)
            return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['user_id'] = logged_user.id

            request.session['first_name'] = logged_user.first_name

            return redirect('/index')


def loginform(request):
    return render(request, 'loginform.html')


def logout(request):
    request.session.delete()
    return redirect('/')
