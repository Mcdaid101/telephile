from . import views
from django.urls import path

urlpatterns = [
    path('', views.PostList.as_view(), name='home'),
    path('<slug:slug>/', views.PostDetail.as_view(), name='post_detail'),
    path('like/<slug:slug>', views.PostLike.as_view(), name='post_like'),
    path('about', views.about, name='about'),
    path('drama', views.drama, name='drama'),
    path('scifi', views.scifi, name='scifi'),
    path('fantasy', views.fantasy, name='fantasy'),
    path('comedy', views.comedy, name='comedy'),
    path('documentary', views.documentary, name='documentary'),
]