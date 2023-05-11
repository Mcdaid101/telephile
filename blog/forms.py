from .models import Comment
from django import forms 


class CommentForm(forms.modelForm):
    class Meta:
        model = Comment
        fields = ('body',)