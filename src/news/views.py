from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, Category, Reporter, Tag
from comments.forms import CommentForm


class ArticleListView(ListView):
    """View for listing articles on the home page"""
    model = Article
    template_name = "news/home.html"
    context_object_name = "latest_articles"
    paginate_by = 5
    
    def get_queryset(self):
        """Get only published articles"""
        return Article.objects.filter(status="published")
    
    def get_context_data(self, **kwargs):
        """Add categories and recent articles to context"""
        context = super().get_context_data(**kwargs)
        context["categories"] = Category.objects.all()
        context["recent_articles"] = Article.objects.filter(
            status="published"
        ).order_by("-published_date")[:5]
        return context


class ArticleDetailView(DetailView):
    """View for displaying a single article"""
    model = Article
    template_name = "news/article_detail.html"
    context_object_name = "article"
    
    def get_queryset(self):
        """Get only published articles"""
        return Article.objects.filter(status="published")
    
    def get_context_data(self, **kwargs):
        """Add related articles and comment form to context"""
        context = super().get_context_data(**kwargs)
        article = self.get_object()
        
        # Get related articles from the same category
        context["related_articles"] = Article.objects.filter(
            category=article.category, 
            status="published"
        ).exclude(id=article.id)[:3]
        
        # Add categories and recent articles for sidebar
        context["categories"] = Category.objects.all()
        context["recent_articles"] = Article.objects.filter(
            status="published"
        ).order_by("-published_date")[:5]
        
        # Add comment form
        context['comment_form'] = CommentForm()
        
        return context


class CategoryDetailView(ListView):
    """View for displaying articles in a category"""
    template_name = "news/category_detail.html"
    context_object_name = "articles"
    paginate_by = 5
    
    def get_queryset(self):
        """Get articles in the selected category"""
        self.category = get_object_or_404(Category, slug=self.kwargs["slug"])
        return Article.objects.filter(category=self.category, status="published")
    
    def get_context_data(self, **kwargs):
        """Add category and sidebar info to context"""
        context = super().get_context_data(**kwargs)
        context["category"] = self.category
        
        # Add categories and recent articles for sidebar
        context["categories"] = Category.objects.all()
        context["recent_articles"] = Article.objects.filter(
            status="published"
        ).order_by("-published_date")[:5]
        
        return context


class ReporterDetailView(ListView):
    """View for displaying a reporter's profile and articles"""
    template_name = "news/reporter_detail.html"
    context_object_name = "articles"
    paginate_by = 5
    
    def get_queryset(self):
        """Get articles by the selected reporter"""
        self.reporter = get_object_or_404(Reporter, pk=self.kwargs["pk"])
        return Article.objects.filter(reporter=self.reporter, status="published")
    
    def get_context_data(self, **kwargs):
        """Add reporter and sidebar info to context"""
        context = super().get_context_data(**kwargs)
        context["reporter"] = self.reporter
        
        # Add categories and recent articles for sidebar
        context["categories"] = Category.objects.all()
        context["recent_articles"] = Article.objects.filter(
            status="published"
        ).order_by("-published_date")[:5]
        
        return context


class TagDetailView(ListView):
    """View for displaying articles with a specific tag"""
    template_name = "news/tag_detail.html"
    context_object_name = "articles"
    paginate_by = 5
    
    def get_queryset(self):
        """Get articles with the selected tag"""
        self.tag = get_object_or_404(Tag, slug=self.kwargs["slug"])
        return self.tag.articles.filter(status="published")
    
    def get_context_data(self, **kwargs):
        """Add tag and sidebar info to context"""
        context = super().get_context_data(**kwargs)
        context["tag"] = self.tag
        
        # Add categories and recent articles for sidebar
        context["categories"] = Category.objects.all()
        context["recent_articles"] = Article.objects.filter(
            status="published"
        ).order_by("-published_date")[:5]
        
        return context


def article_detail(request, pk):
    article = get_object_or_404(Article, pk=pk)
    comment_form = CommentForm()
    return render(request, 'news/article_detail.html', {
        'article': article,
        'comment_form': comment_form,
    })