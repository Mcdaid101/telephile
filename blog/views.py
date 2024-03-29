from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import Post, Category
from .forms import CommentForm, reviewForm
from django.urls import reverse
from django.template import loader
from django.views.generic import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test, login_required
from functools import wraps


def user_is_post_author(view_func):
    @wraps(view_func)
    def wrapper(request, post_id, *args, **kwargs):
        post = get_object_or_404(Post, id=post_id)

        if request.user == post.author:
            return view_func(request, post_id, *args, **kwargs)
        else:
            return redirect('home')  

    return wrapper


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class AddPostView(CreateView, LoginRequiredMixin):
    """
    Allows user to post their own review
    """
    form_class = reviewForm
    template_name = 'add_post.html'

    def get_success_url(self):
        return reverse('add_post')

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.slug = slugify(form.cleaned_data['title'])

        return super().form_valid(form)


@user_is_post_author
def DeletePost(request, post_id):
    """
    delete your post
    """
    post = Post.objects.get(pk=post_id)
    context = {'post': post}

    if request.method == 'POST':
        post.delete()
        messages.success(request, f'You have deleted your review successfully')
        return redirect('your_reviews')

    return render(request, 'delete_post.html', context)


@user_is_post_author
def EditPost(request, post_id):
    """
    edit a post
    """
    post = get_object_or_404(Post, pk=post_id)
    if request.method == 'POST':
        form = reviewForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, "Successfully edited review")
            return redirect(reverse('post_detail', args=[post.slug]))
        else:
            messages.error(request, f'Failed to edit your review')
    else:
        form = reviewForm(instance=post)

    template = 'edit_post.html'
    context = {
        'form': form,
        'post': post,
    }
    return render(request, template, context)


class PostDetail(View):
    """
    Post details, view once posts are clicked on to read more
    """

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


class PostLike(View):
    """
    View which gives the ability for users to like and unlike posts
    """
    def post(self, request, slug, *args, **kwargs):
        post = get_object_or_404(Post, slug=slug)
        if post.likes.filter(id=request.user.id).exists():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        return HttpResponseRedirect(reverse('post_detail', args=[slug]))


def about(request):
    """
    Renders the about page
    """
    return render(request, 'about.html')


def drama(request):
    """
    This renders the drama category page with any posts within that category
    """
    view = Post.objects.filter(category__category="Drama", status=1)
    return render(request, 'categories.html', {'view': view})


def scifi(request):
    """
    This renders the sci-fi category page with any posts within that category
    """
    view = Post.objects.filter(category__category="Sci-Fi", status=1)
    return render(request, 'categories.html', {'view': view})


def fantasy(request):
    """
    This renders the fantasy category page with any posts within that category
    """
    view = Post.objects.filter(category__category="Fantasy", status=1)
    return render(request, 'categories.html', {'view': view})


def comedy(request):
    """
    This renders the comedy category page with any posts within that category
    """
    view = Post.objects.filter(category__category="Comedy", status=1)
    return render(request, 'categories.html', {'view': view})


def documentary(request):
    """
    This renders the documentary category page with any posts
    within that category
    """
    view = Post.objects.filter(category__category="Documentary", status=1)
    return render(request, 'categories.html', {'view': view})


def yourReviews(request):
    """
    This renders the users own reviews
    """
    user = request.user
    view = Post.objects.filter(author=user, status=1)
    return render(request, 'your_reviews.html', {'view': view})
