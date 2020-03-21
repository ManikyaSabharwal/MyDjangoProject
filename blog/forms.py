from django import forms
from blog.models import Comment
from django.contrib.auth.models import User

from .models import Post

class PostForm(forms.ModelForm):
    #Which model to use
    class Meta:
        model = Post
        fields = ('title', 'text',)

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    class Meta():
        model = User
        fields = ('username','password')

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('comment',)