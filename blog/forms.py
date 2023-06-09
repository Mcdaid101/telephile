from .models import Comment, Post
from django import forms 


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('body',)


class reviewForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'content', 'category',)
        widgets = {
            'title': forms.TextInput(),
            'content': forms.TextInput(attrs={'style': 'height:400px'}),
            'category': forms.Select(),
            }
