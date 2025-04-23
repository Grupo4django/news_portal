from django.urls import path
from . import views

app_name = "news"

urlpatterns = [
    # Home page with latest articles
    path("", views.ArticleListView.as_view(), name="home"),
    
    # Article detail page
    path("article/<slug:slug>/", views.ArticleDetailView.as_view(), name="article_detail"),
    
    # Category pages
    path("category/<slug:slug>/", views.CategoryDetailView.as_view(), name="category_detail"),
    
    # Reporter pages
    path("reporter/<int:pk>/", views.ReporterDetailView.as_view(), name="reporter_detail"),
    
    # Tag pages
    path("tag/<slug:slug>/", views.TagDetailView.as_view(), name="tag_detail"),
]