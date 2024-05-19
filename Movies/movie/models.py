from django.contrib.auth.models import User
from django.db import models


class Category(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='category_images')
    description= models.TextField()

    def __str__(self):
        return self.name


class Movie(models.Model):
    name=models.CharField(max_length=200)
    image=models.ImageField(upload_to='movie_images/')
    release_date= models.DateField()
    description= models.TextField()
    actors = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    trailer_link=models.URLField()
    posted=models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Comment(models.Model):
    moviename=models.ForeignKey(Movie,on_delete=models.CASCADE)
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    comment=models.TextField()

    def __str__(self):
        return f'Comment by {self.user.username} on {self.moviename.name}'
class Rating(models.Model):
    moviename = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating=models.PositiveSmallIntegerField()

    def __str__(self):
        return f'Rating of {self.rating} by {self.user.username} for {self.moviename.name}'


