from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

class CustomUser(User):
    pass

class addrecipe(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    img = models.FileField(upload_to='images')
    ingredients = models.CharField(max_length=30)
    procedure = models.CharField(max_length=30)

class Comment(models.Model):
    recipe = models.ForeignKey(addrecipe, related_name='comments', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.recipe.name}'
    
    
class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True)
    email = models.EmailField()
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.user.username
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('follower', 'followed')
        verbose_name = 'Follow'
        verbose_name_plural = 'Follows'

    def _str_(self):
        return f"{self.follower} follows {self.followed}"
    

class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, related_name='notifications', on_delete=models.CASCADE)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification for {self.user.username} - Comment on {self.comment.recipe.name}'
    
class Saves(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(addrecipe, on_delete=models.CASCADE)

class Rating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(addrecipe, on_delete=models.CASCADE)
    rating = models.DecimalField(
        max_digits=2,  # Total digits (including decimals)
        decimal_places=1,  # Digits after the decimal point
        validators=[
            MinValueValidator(0.5),
            MaxValueValidator(5.0),
        ]
    )
    class Meta:
        unique_together = ('recipe', 'user')

class NormalizedRatingParameters(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    std=models.FloatField()
    mean=models.FloatField()


    
    

    


