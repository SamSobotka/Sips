from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# UserManager
class UserManager(BaseUserManager):
    def create_user(self, email, handle, password=None, **extra_fields):
        if not handle:
            raise ValueError("User must have a valid handle")

        user = self.model(handle=handle, email=self.normalize_email(email))
        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, email, handle, password=None, **extra_fields):
        if not handle:
            raise ValueError("User must have a valid handle")

        user = self.model(handle=handle, email=self.normalize_email(email), is_superuser=True)
        user.set_password(password)
        user.save(using=self.db)
        return user
# End UserManager


# User
class User(AbstractBaseUser, PermissionsMixin):
    userid = models.AutoField(
        db_column='userID',
        primary_key=True
    )
    handle = models.CharField(unique=True, max_length=20)
    bio = models.TextField(blank=True, default='Hello! I\'m a new Sips user!')
    password = models.CharField(max_length=25)
    points = models.IntegerField(blank=True, default=0)
    email = models.EmailField(max_length=50, unique=True)

    # special user attributes
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def check_password(self, raw_password):
        return self.password == raw_password

    class Meta:
        db_table = 'User'
        db_table_comment = 'hosts basic user information'
# End User


# Follow
class Follow(models.Model):
    hostid = models.ForeignKey('User', models.CASCADE, db_column='hostID', related_name='host_set')
    followerid = models.ForeignKey('User', models.CASCADE, db_column='followerID', related_name='follower_set')

    class Meta:
        db_table = 'Follow'
        unique_together = (('hostid', 'followerid'),)
# End Follow


# Post
class Post(models.Model):
    postid = models.BigAutoField(
        db_column='postID',
        primary_key=True
    )
    userid = models.ForeignKey('User', models.CASCADE, db_column='userID')
    content = models.TextField()
    title = models.CharField(max_length=50)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        db_table = 'Post'
# End Post


# FeedBuilder
class Feedbuilder(models.Model):
    userid = models.ForeignKey('User', models.CASCADE, db_column='userID')
    postid = models.ForeignKey('Post', models.CASCADE, db_column='postID')

    class Meta:
        db_table = 'FeedBuilder'
        unique_together = (('userid', 'postid'),)
# End FeedBuilder


# Comment
class Comment(models.Model):
    commentid = models.BigAutoField(
        db_column='commentID',
        primary_key=True
    )
    postid = models.ForeignKey('Post', models.CASCADE, db_column='postID')
    userid = models.ForeignKey('User', models.CASCADE, db_column='userID')
    content = models.TextField()
    likes = models.ManyToManyField(User, related_name='liked_comments', blank=True)

    class Meta:
        db_table = 'Comment'
# End Comment


# Item
class Item(models.Model):
    itemname = models.CharField(choices=(
        ('theme_darkmode', 'Dark Mode'),
        ('theme_highcontrast', 'High Contrast'),
        ('theme_custom', 'Custom Theme')  # add more here and migrate
    ), max_length=20, db_column='itemName')
    cost = models.IntegerField(default=0)
    description = models.CharField(max_length=40, null=True)

    class Meta:
        db_table = 'Item'
# End Item


# Transaction
class Transaction(models.Model):
    transactionid = models.BigAutoField(
        db_column='transactionID',
        primary_key=True
    )
    userid = models.ForeignKey('User', models.CASCADE, db_column='userID')
    itemid = models.ForeignKey('Item', models.CASCADE, db_column='itemID')

    class Meta:
        db_table = 'Transaction'
# End Transaction


# Message
class Message(models.Model):
    messageid = models.BigAutoField(
        db_column='messageID',
        primary_key=True
    )
    senderid = models.ForeignKey('User', models.CASCADE, db_column='senderID', related_name='sender_set')
    recipientid = models.ForeignKey('User', models.CASCADE, db_column='recipientID', related_name='recipient_set')
    content = models.TextField()
    date_created = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'Message'
# End Message
