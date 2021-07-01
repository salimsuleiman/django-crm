from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save


class User(AbstractUser):
    is_organizer = models.BooleanField(default=False)
    is_agent = models.BooleanField(default=True)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Lead(models.Model):
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey(
        'Agent', on_delete=models.SET_NULL, null=True, blank=True)
    organization = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(
        'Category', related_name='leads', blank=True,  null=True, on_delete=models.SET_NULL)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()

    def __str__(self):
        return f'{self.first_name}'


class Agent(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    organization = models.ForeignKey(
        'UserProfile', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username}'
            


class Category(models.Model):
    name = models.CharField(max_length=30)
    organization = models.ForeignKey(
        'UserProfile',
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


def post_user_create_signal(sender, instance, created, **kwargs):
    if created:
        if instance.is_organizer:
            UserProfile.objects.create(user=instance)
            print('New user is created :0')


post_save.connect(post_user_create_signal, sender=User)

