from django.shortcuts import render, get_object_or_404
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Post, Category
from .forms import CommentForm, reviewForm
from django.urls import reverse
from django.template import loader
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


"""
Allows user to post their own review
"""
class AddPostView(CreateView, LoginRequiredMixin):
    form_class = reviewForm
    template_name = 'add_post.html'
    
    def get_success_url(self):
        return reverse('add_post')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])

        return super().form_valid(form)


"""
Post details, view once posts are clicked on to read more
"""
class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
      
        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": False,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )


    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
        else:
            comment_form = CommentForm()

        return render(
            request,
            "post_detail.html",
            {
                "post": post,
                "comments": comments,
                "commented": True,
                "liked": liked,
                "comment_form": CommentForm()
            },
        )

"""
View which gives the ability for users to like and unlike posts
"""
class PostLike(View):
    
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


"""
Renders the about page
"""
def about(request):
    return render(request, 'about.html')


"""
This renders the drama category page with any posts within that category
"""
def drama(request):
    view = Post.objects.filter(category__category="Drama", status=1)
    return render(request, 'categories.html', {'view': view})


"""
This renders the sci-fi category page with any posts within that category
"""
def scifi(request):
    view = Post.objects.filter(category__category="Sci-Fi", status=1)
    return render(request, 'categories.html', {'view': view}), 


"""
This renders the fantasy category page with any posts within that category
"""
def fantasy(request):
    view = Post.objects.filter(category__category="Fantasy", status=1)
    return render(request, 'categories.html', {'view': view})


"""
This renders the comedy category page with any posts within that category
"""
def comedy(request):
    view = Post.objects.filter(category__category="Comedy", status=1)
    return render(request, 'categories.html', {'view': view})


"""
This renders the documentary category page with any posts within that category
"""
def documentary(request):
    view = Post.objects.filter(category__category="Documentary", status=1)
    return render(request, 'categories.html', {'view': view})

"""
This renders the users own reviews
"""
def yourReviews(request):
    user = request.user
    view = Post.objects.filter(author=user, status=1)
    return render(request, 'your_reviews.html', {'view': view})