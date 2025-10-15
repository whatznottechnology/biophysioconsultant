from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    # Blog list and search
    path('', views.BlogListView.as_view(), name='blog_list'),
    path('search/', views.blog_search, name='blog_search'),
    
    # Category pages
    path('category/<str:category>/', views.BlogCategoryView.as_view(), name='blog_category'),
    
    # Individual blog post
    path('<slug:slug>/', views.BlogDetailView.as_view(), name='post_detail'),
]