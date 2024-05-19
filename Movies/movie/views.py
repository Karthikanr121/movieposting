from django.contrib import messages, auth
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404

from .models import Category, Movie, Comment, Rating

def movie_list(request):
    query=request.GET.get('q')
    if query:
        movies=Movie.objects.filter(name__icontains=query)
    else:
        movies=Movie.objects.all()

    return render(request,'movie_list.html',{'movies': movies})
# Create your views here.
def movie_detail(request,pk):
    movie=get_object_or_404(Movie, pk=pk)
    comments = Comment.objects.filter(moviename=movie.pk)
    rating=Rating.objects.filter(moviename=movie.pk)
    context = {
        'movie': movie,
        'comments': comments,
        'rating': rating,
    }
    return render(request, 'movie_detail.html', context)


def category_movies(request,category_id):
    category= Category.objects.get(pk=category_id)
    movies=Movie.objects.filter(category=category)
    return render(request,'category_movies.html',{'category':category,'movies':movies})

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            messages.info(request,"Invallid credentials")
            return redirect('login')
    return render(request,"login.html")
def register(request):
    if request.method == 'POST':
        username=request.POST['username']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        email = request.POST['email']
        password = request.POST['password']
        confirm = request.POST['password1']
        if password==confirm:
            if User.objects.filter(username=username).exists():
                messages.info(request,"Username taken")
                return redirect('register')
            elif User.objects.filter(email=email).exists():
                messages.info(request,"Email taken")
                return redirect('register')
            else:
                user=User.objects.create_user(username=username,password=password,first_name=first_name,last_name=last_name,email=email)
                user.save();
                return redirect('login')
        else:
            messages.info(request,"Password not matching")
            return redirect('register')

    return render(request,"register.html")
def logout(request):
    auth.logout(request)
    return redirect('/')

def add_movie(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        release_date = request.POST.get('release_date')
        description = request.POST.get('description')
        image = request.FILES.get('image')
        actors = request.POST.get('actors')
        category_id = request.POST.get('category')
        trailer_link = request.POST.get('trailer_link')
        posted = request.user

        category=Category.objects.get(pk=category_id)
        movie = Movie.objects.create(name=name, release_date=release_date, description=description, image=image,
                                     actors=actors, category=category, trailer_link=trailer_link, posted=posted)
        movie.save()
        return redirect('movie_list')
    else:
        categories = Category.objects.all()
        return render(request, 'add_movie.html', {'categories': categories})
    return render(request,'add_movie.html')

def delete_movie(request,pk):
    movie=Movie.objects.get(pk=pk)
    if request.method == 'POST':
        if request.user == movie.posted:
            movie.delete()
        return redirect('movie_list')
    return render(request, 'delete_movie.html', {'movie': movie})

def update_movie(request, pk):
    movie = get_object_or_404(Movie, pk=pk)

    if request.user != movie.posted:
        return redirect('movie_list')

    categories = Category.objects.all()

    if request.method == 'POST':
        name = request.POST['name']
        release_date = request.POST['release_date']
        description = request.POST['description']
        actors = request.POST['actors']
        category_id = request.POST['category']
        trailer_link = request.POST['trailer_link']

        movie.name = name
        movie.release_date = release_date
        movie.description = description
        movie.actors = actors
        movie.category = Category.objects.get(id=category_id)
        movie.trailer_link = trailer_link

        if 'image' in request.FILES:
            movie.image = request.FILES['image']

        movie.save()
        return redirect('movie_detail', pk=movie.pk)

    return render(request, 'update_movie.html', {'movie': movie, 'categories': categories})

def view_profile(request):
    if request.method == 'POST':
        user = request.user
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.save()
        return redirect('movie_list')
    return render(request, 'view_profile.html', {'user': request.user})

def add_comment(request, movie_id):
    moviename = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        comment = request.POST.get('text', '')
        if comment:
            comments = Comment.objects.create(moviename=moviename, user=request.user, comment=comment)
            return redirect('movie_detail', pk=moviename.pk)
    return render(request, 'movie_detail.html', {'moviename': moviename})


# def add_comment(request, movie_id):
#     moviename = get_object_or_404(Movie, pk=movie_id)
#     if request.method == 'POST':
#         text = request.POST['text']
#         comment = Comment.objects.create(moviename=moviename, user=request.user, text=text)
#         return redirect('movie_detail', pk=moviename.pk)
#     return render(request, 'add_comment.html', {'moviename': moviename})

def add_rating(request, movie_id):
    moviename = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        rating_value = int(request.POST['rating'])
        rating, created = Rating.objects.update_or_create(
            moviename=moviename,
            user=request.user,
            defaults={'rating': rating_value}
        )
        return redirect('movie_detail', pk=moviename.pk)
    return render(request, 'add_rating.html', {'moviename': moviename})