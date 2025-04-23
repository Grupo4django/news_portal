# Django News Portal with Templates and Admin 📰

## Description 📝

This guide walks you through building a news portal using Django's template system and admin interface. You'll create a web application that allows administrators to manage news articles, categories, and reporters while showcasing these articles to readers. By the end, you'll understand how to leverage Django's template engine for dynamic content presentation and customize the admin interface for an efficient content management experience.

## Table of Contents 📋

- [Django News Portal with Templates and Admin 📰](#django-news-portal-with-templates-and-admin-)
  - [Description 📝](#description-)
  - [Table of Contents 📋](#table-of-contents-)
  - [Understanding the Concept 🧠](#understanding-the-concept-)
    - [The Django Template System](#the-django-template-system)
    - [Django Admin Interface](#django-admin-interface)
    - [Why a News Portal?](#why-a-news-portal)
    - [Application Structure](#application-structure)
  - [Environment Setup 🛠️](#environment-setup-️)
  - [Implementation 🚀](#implementation-)
    - [Step 1: Project Creation](#step-1-project-creation)
    - [Step 2: Creating the News App](#step-2-creating-the-news-app)
    - [Step 3: Defining Models](#step-3-defining-models)
    - [Step 4: Configure Admin Interface](#step-4-configure-admin-interface)
    - [Step 5: Creating Base Templates](#step-5-creating-base-templates)
    - [Step 6: Implementing Article Views](#step-6-implementing-article-views)
    - [Step 8: Implementing Template Filters](#step-8-implementing-template-filters)
  - [Testing Your Application 🧪](#testing-your-application-)
    - [Writing Model Tests](#writing-model-tests)
  - [Applications to Extend Functionality 💡](#applications-to-extend-functionality-)
    - [1. Comments App](#1-comments-app)
    - [2. User Profiles App](#2-user-profiles-app)
    - [3. Newsletter App](#3-newsletter-app)
  - [Next Steps 🚶](#next-steps-)

## Understanding the Concept 🧠

### The Django Template System

Django's template system is a powerful tool for generating dynamic HTML content. It allows you to separate the design from Python code, making your application more maintainable. Key features include:

1. **Variables** - Display dynamic content using `{{ variable }}` syntax
2. **Tags** - Control flow with `{% tag %}` syntax (if, for, block, etc.)
3. **Filters** - Modify variables using the pipe symbol: `{{ variable|filter }}`
4. **Template Inheritance** - Create a base layout and extend it in child templates
5. **Include** - Insert reusable template fragments with `{% include "template.html" %}`

The template system follows the DRY (Don't Repeat Yourself) principle, allowing you to maintain consistent layouts across your site.

### Django Admin Interface

Django's admin interface is a built-in application that provides content management functionality with almost no code. It reads metadata from your models to provide a production-ready interface for managing content. Key features include:

1. **Automatic Form Generation** - Forms created automatically from model definitions
2. **CRUD Operations** - Create, read, update, and delete functionality built-in
3. **Customization** - Easily customizable with options for field display, filtering, and search
4. **User Authentication** - Built-in user authentication and permission management
5. **List and Detail Views** - Organized views for listing and editing records

### Why a News Portal?

A news portal is an excellent project for learning Django templates and admin because:

1. It has clear content models (articles, categories, authors)
2. It requires dynamic content presentation
3. It benefits from a robust admin interface for content editors
4. It uses various template features (inheritance, filters, includes)
5. It demonstrates practical real-world application of Django's strengths

### Application Structure

Our news portal will have the following components:

```
news_portal/                  # Project root
├── src/                      # Source code directory
│   ├── config/               # Project settings
│   ├── news/                 # News application
│   │   ├── models.py         # Data models
│   │   ├── admin.py          # Admin configuration
│   │   ├── views.py          # View functions
│   │   ├── urls.py           # URL patterns
│   │   ├── templatetags/     # Custom template tags/filters
│   │   └── templates/        # HTML templates
│   │       ├── base.html     # Base template
│   │       ├── home.html     # Homepage
│   │       ├── article.html  # Article detail
│   │       └── category.html # Category listing
│   ├── static/               # Static files (CSS, JS)
│   └── media/                # User-uploaded content
├── venv/                     # Virtual environment
└── requirements.txt          # Python dependencies
```

## Environment Setup 🛠️

Let's set up our development environment:

```bash
# Create project directory
mkdir news_portal
cd news_portal

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows, use: venv\Scripts\activate

# Create src directory (modern Django project structure)
mkdir src
cd src

# Install Django and Pillow (for image handling)
pip3 install django pillow

# Create requirements file
pip3 freeze > requirements.txt
```

Create a `.gitignore` file in the project root:

```bash
# Return to project root
cd ..

# Create .gitignore
cat > .gitignore << EOL
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Django
*.log
local_settings.py
db.sqlite3
db.sqlite3-journal
media/

# Virtual Environment
venv/
ENV/

# IDE
.idea/
.vscode/
*.swp
*.swo

# OS specific
.DS_Store
Thumbs.db
EOL
```

## Implementation 🚀

### Step 1: Project Creation

Create a new Django project:

```bash
# Navigate to src directory
cd src

# Create Django project
django-admin startproject config .
```

### Step 2: Creating the News App

Create a new app for our news portal:

```bash
# Create news app
python3 manage.py startapp news
```

Register the app in `config/settings.py`:

```python
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'news',  # Our news app
]

# Add the following at the end of the file
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

Update `config/urls.py` to include the news app URLs and serve media files:

```python
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('news.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
```

### Step 3: Defining Models

Create models in `news/models.py`:

```python
from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.urls import reverse


class Category(models.Model):
    """Category model for organizing articles"""
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    
    class Meta:
        verbose_name_plural = "categories"
        ordering = ["name"]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("news:category_detail", kwargs={"slug": self.slug})


class Reporter(models.Model):
    """Reporter/author model"""
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    avatar = models.ImageField(upload_to="reporters/", blank=True)
    
    def __str__(self):
        return self.user.get_full_name() or self.user.username
    
    def get_absolute_url(self):
        return reverse("news:reporter_detail", kwargs={"pk": self.pk})


class Article(models.Model):
    """News article model"""
    STATUS_CHOICES = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    summary = models.TextField(blank=True)
    image = models.ImageField(upload_to="articles/", blank=True)
    published_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="draft")
    
    # Relationships
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles")
    reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE, related_name="articles")
    
    class Meta:
        ordering = ["-published_date"]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if not self.summary and self.content:
            # Create a summary from the first 100 words of content
            words = self.content.split()[:100]
            self.summary = " ".join(words) + "..."
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("news:article_detail", kwargs={"slug": self.slug})


class Tag(models.Model):
    """Tag model for articles"""
    name = models.CharField(max_length=50)
    slug = models.SlugField(unique=True)
    
    # Relationship
    articles = models.ManyToManyField(Article, related_name="tags")
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse("news:tag_detail", kwargs={"slug": self.slug})
```

Create and apply migrations:

```bash
# Create migrations
python3 manage.py makemigrations

# Apply migrations
python3 manage.py migrate
```

### Step 4: Configure Admin Interface

Configure the admin interface in `news/admin.py`:

```python
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Reporter, Article, Tag


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """Admin configuration for categories"""
    list_display = ("name", "slug", "article_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")
    
    def article_count(self, obj):
        """Count articles in this category"""
        count = obj.articles.count()
        return count if count > 0 else "-"
    article_count.short_description = "Articles"


class TagInline(admin.TabularInline):
    """Inline admin for tags"""
    model = Tag.articles.through
    extra = 1


@admin.register(Reporter)
class ReporterAdmin(admin.ModelAdmin):
    """Admin configuration for reporters"""
    list_display = ("user", "display_name", "article_count")
    search_fields = ("user__username", "user__first_name", "user__last_name", "bio")
    
    def display_name(self, obj):
        """Display reporter's full name"""
        return obj.user.get_full_name() or obj.user.username
    display_name.short_description = "Name"
    
    def article_count(self, obj):
        """Count articles by this reporter"""
        count = obj.articles.count()
        return count if count > 0 else "-"
    article_count.short_description = "Articles"


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """Admin configuration for articles"""
    list_display = ("title", "reporter", "category", "status", "published_date", "display_image")
    list_filter = ("status", "category", "published_date", "reporter")
    search_fields = ("title", "content", "reporter__user__username")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "published_date"
    inlines = [TagInline]
    
    fieldsets = (
        ("Content", {
            "fields": ("title", "slug", "content", "summary", "image")
        }),
        ("Publishing", {
            "fields": ("status", "category", "reporter")
        }),
    )
    
    def display_image(self, obj):
        """Display article image"""
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" style="object-fit: cover;" />', obj.image.url)
        return "No image"
    display_image.short_description = "Image"


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """Admin configuration for tags"""
    list_display = ("name", "slug", "article_count")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name",)
    
    def article_count(self, obj):
        """Count articles with this tag"""
        count = obj.articles.count()
        return count if count > 0 else "-"
    article_count.short_description = "Articles"
```

### Step 5: Creating Base Templates

First, create the templates directory structure:

```bash
mkdir -p news/templates/news
touch news/templates/news/base.html
touch news/templates/news/home.html
touch news/templates/news/article_detail.html
touch news/templates/news/category_detail.html
touch news/templates/news/reporter_detail.html
touch news/templates/news/tag_detail.html
```

Create a base template in `news/templates/news/base.html`:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Django News Portal{% endblock %}</title>
    <style>
        /* Basic CSS for readability */
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
        }
        header {
            background-color: #2c3e50;
            color: white;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        nav ul {
            display: flex;
            list-style: none;
            padding: 0;
            margin: 0;
        }
        nav li {
            margin-right: 1rem;
        }
        nav a {
            color: white;
            text-decoration: none;
        }
        nav a:hover {
            text-decoration: underline;
        }
        .container {
            display: flex;
            flex-wrap: wrap;
        }
        main {
            flex: 3;
            min-width: 60%;
        }
        aside {
            flex: 1;
            min-width: 250px;
            margin-left: 1rem;
            background-color: #f5f5f5;
            padding: 1rem;
            border-radius: 4px;
        }
        .article-card {
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 1rem;
            margin-bottom: 1rem;
        }
        .article-card img {
            max-width: 100%;
            height: auto;
        }
        footer {
            background-color: #2c3e50;
            color: white;
            padding: 1rem;
            margin-top: 2rem;
            text-align: center;
        }
    </style>
    {% block extra_css %}{% endblock %}
</head>
<body>
    <header>
        <h1><a href="{% url 'news:home' %}" style="color: white; text-decoration: none;">Django News Portal</a></h1>
        <nav>
            <ul>
                <li><a href="{% url 'news:home' %}">Home</a></li>
                <li><a href="{% url 'admin:index' %}">Admin</a></li>
                {% block nav_items %}{% endblock %}
            </ul>
        </nav>
    </header>
    
    <div class="container">
        <main>
            {% block content %}
            <!-- Main content will go here -->
            {% endblock %}
        </main>
        
        <aside>
            <h3>Categories</h3>
            <ul>
                {% block categories_sidebar %}
                    {% for category in categories %}
                        <li><a href="{{ category.get_absolute_url }}">{{ category.name }}</a></li>
                    {% empty %}
                        <li>No categories available</li>
                    {% endfor %}
                {% endblock %}
            </ul>
            
            <h3>Recent Articles</h3>
            <ul>
                {% block recent_articles %}
                    {% for article in recent_articles %}
                        <li><a href="{{ article.get_absolute_url }}">{{ article.title }}</a></li>
                    {% empty %}
                        <li>No recent articles</li>
                    {% endfor %}
                {% endblock %}
            </ul>
        </aside>
    </div>
    
    <footer>
        <p>&copy; {% now "Y" %} Django News Portal - A learning project</p>
    </footer>
</body>
</html>
```

Create a home template in `news/templates/news/home.html`:

```html
{% extends "news/base.html" %}

{% block title %}Home - Django News Portal{% endblock %}

{% block content %}
    <h2>Latest News</h2>
    
    {% for article in latest_articles %}
        <div class="article-card">
            <h3><a href="{{ article.get_absolute_url }}">{{ article.title }}</a></h3>
            
            <div class="article-meta">
                <span>By <a href="{{ article.reporter.get_absolute_url }}">{{ article.reporter }}</a></span>
                <span>in <a href="{{ article.category.get_absolute_url }}">{{ article.category }}</a></span>
                <span>on {{ article.published_date|date:"F j, Y" }}</span>
            </div>
            
            {% if article.image %}
                <img src="{{ article.image.url }}" alt="{{ article.title }}">
            {% endif %}
            
            <p>{{ article.summary }}</p>
            
            <div class="article-tags">
                {% for tag in article.tags.all %}
                    <a href="{{ tag.get_absolute_url }}" style="margin-right: 5px;">#{{ tag.name }}</a>
                {% endfor %}
            </div>
            
            <a href="{{ article.get_absolute_url }}">Read more</a>
        </div>
    {% empty %}
        <p>No articles available.</p>
    {% endfor %}
    
    {% if is_paginated %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page=1">&laquo; first</a>
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}
            
            <span>
                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
            </span>
            
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
```

Create an article detail template in `news/templates/news/article_detail.html`:

```html
{% extends "news/base.html" %}

{% block title %}{{ article.title }} - Django News Portal{% endblock %}

{% block content %}
    <article>
        <h2>{{ article.title }}</h2>
        
        <div class="article-meta">
            <span>By <a href="{{ article.reporter.get_absolute_url }}">{{ article.reporter }}</a></span>
            <span>in <a href="{{ article.category.get_absolute_url }}">{{ article.category }}</a></span>
            <span>on {{ article.published_date|date:"F j, Y" }}</span>
            
            {% if article.updated_date != article.published_date %}
                <span>(Updated: {{ article.updated_date|date:"F j, Y H:i" }})</span>
            {% endif %}
        </div>
        
        {% if article.image %}
            <img src="{{ article.image.url }}" alt="{{ article.title }}" 
                 style="max-width: 100%; margin: 1rem 0;">
        {% endif %}
        
        <div class="article-content">
            {{ article.content|linebreaks }}
        </div>
        
        <div class="article-tags">
            <h4>Tags:</h4>
            {% for tag in article.tags.all %}
                <a href="{{ tag.get_absolute_url }}" style="margin-right: 5px;">#{{ tag.name }}</a>
            {% empty %}
                <span>No tags for this article</span>
            {% endfor %}
        </div>
    </article>
    
    <div class="related-articles">
        <h3>More from {{ article.category }}</h3>
        <ul>
            {% for related in related_articles %}
                <li><a href="{{ related.get_absolute_url }}">{{ related.title }}</a></li>
            {% empty %}
                <li>No related articles found</li>
            {% endfor %}
        </ul>
    </div>
{% endblock %}
```

Create a category detail template in `news/templates/news/category_detail.html`:

```html
{% extends "news/base.html" %}

{% block title %}{{ category.name }} - Django News Portal{% endblock %}

{% block content %}
    <h2>{{ category.name }}</h2>
    
    {% if category.description %}
        <p>{{ category.description }}</p>
    {% endif %}
    
    <h3>Articles in this category:</h3>
    
    {% for article in articles %}
        <div class="article-card">
            <h3><a href="{{ article.get_absolute_url }}">{{ article.title }}</a></h3>
            
            <div class="article-meta">
                <span>By <a href="{{ article.reporter.get_absolute_url }}">{{ article.reporter }}</a></span>
                <span>on {{ article.published_date|date:"F j, Y" }}</span>
            </div>
            
            {% if article.image %}
                <img src="{{ article.image.url }}" alt="{{ article.title }}">
            {% endif %}
            
            <p>{{ article.summary }}</p>
            <a href="{{ article.get_absolute_url }}">Read more</a>
        </div>
    {% empty %}
        <p>No articles in this category yet.</p>
    {% endfor %}
    
    {% if is_paginated %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page=1">&laquo; first</a>
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}
            
            <span>
                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
            </span>
            
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
```

Create a reporter detail template in `news/templates/news/reporter_detail.html`:

```html
{% extends "news/base.html" %}

{% block title %}{{ reporter }} - Django News Portal{% endblock %}

{% block content %}
    <div class="reporter-profile">
        <h2>{{ reporter }}</h2>
        
        {% if reporter.avatar %}
            <img src="{{ reporter.avatar.url }}" alt="{{ reporter }}" 
                 style="width: 150px; height: 150px; object-fit: cover; border-radius: 50%;">
        {% endif %}
        
        {% if reporter.bio %}
            <div class="reporter-bio">
                <h3>About the reporter</h3>
                {{ reporter.bio|linebreaks }}
            </div>
        {% endif %}
    </div>
    
    <div class="reporter-articles">
        <h3>Articles by {{ reporter }}</h3>
        
        {% for article in articles %}
            <div class="article-card">
                <h4><a href="{{ article.get_absolute_url }}">{{ article.title }}</a></h4>
                
                <div class="article-meta">
                    <span>in <a href="{{ article.category.get_absolute_url }}">{{ article.category }}</a></span>
                    <span>on {{ article.published_date|date:"F j, Y" }}</span>
                </div>
                
                <p>{{ article.summary }}</p>
                <a href="{{ article.get_absolute_url }}">Read more</a>
            </div>
        {% empty %}
            <p>This reporter hasn't published any articles yet.</p>
        {% endfor %}
    </div>
    
    {% if is_paginated %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page=1">&laquo; first</a>
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}
            
            <span>
                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
            </span>
            
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
```

Create a tag detail template in `news/templates/news/tag_detail.html`:

```html
{% extends "news/base.html" %}

{% block title %}#{{ tag.name }} - Django News Portal{% endblock %}

{% block content %}
    <h2>#{{ tag.name }}</h2>
    
    {% for article in articles %}
        <div class="article-card">
            <h3><a href="{{ article.get_absolute_url }}">{{ article.title }}</a></h3>
            
            <div class="article-meta">
                <span>By <a href="{{ article.reporter.get_absolute_url }}">{{ article.reporter }}</a></span>
                <span>in <a href="{{ article.category.get_absolute_url }}">{{ article.category }}</a></span>
                <span>on {{ article.published_date|date:"F j, Y" }}</span>
            </div>
            
            {% if article.image %}
                <img src="{{ article.image.url }}" alt="{{ article.title }}">
            {% endif %}
            
            <p>{{ article.summary }}</p>
            <a href="{{ article.get_absolute_url }}">Read more</a>
        </div>
    {% empty %}
        <p>No articles with this tag yet.</p>
    {% endfor %}
    
    {% if is_paginated %}
        <div class="pagination">
            {% if page_obj.has_previous %}
                <a href="?page=1">&laquo; first</a>
                <a href="?page={{ page_obj.previous_page_number }}">previous</a>
            {% endif %}
            
            <span>
                Page {{ page_obj.number }} of {{ page_obj.paginator.num_pages }}
            </span>
            
            {% if page_obj.has_next %}
                <a href="?page={{ page_obj.next_page_number }}">next</a>
                <a href="?page={{ page_obj.paginator.num_pages }}">last &raquo;</a>
            {% endif %}
        </div>
    {% endif %}
{% endblock %}
```

### Step 6: Implementing Article Views

Create view functions in `news/views.py`:

```python
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import Article, Category, Reporter, Tag


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
        """Add related articles to context"""
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


### Step 7: Adding URL Patterns

Create a `urls.py` file in the news app:

```python
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
```

### Step 8: Implementing Template Filters

Let's create a custom template filter to truncate text at the word level. First, create the required directory structure:

```bash
mkdir -p news/templatetags
touch news/templatetags/__init__.py
touch news/templatetags/news_extras.py
```

Now create the filter in `news/templatetags/news_extras.py`:

```python
from django import template
import re

register = template.Library()


@register.filter(name="truncate_words_html")
def truncate_words_html(value, arg):
    """
    Truncates HTML to a certain number of words.
    Preserves HTML tags.
    
    Usage: {{ text|truncate_words_html:50 }}
    """
    try:
        length = int(arg)
    except ValueError:
        return value
    
    if not value:
        return ""
    
    # Count words while preserving HTML tags
    words_to_return = length
    
    # Split by spaces but preserve HTML tags
    tag_pattern = r'(<[^>]+>|[^<>\s]+)'
    splitted = re.findall(tag_pattern, value)
    
    # Loop through and count
    result = []
    word_count = 0
    
    for part in splitted:
        if not part.startswith('<'):
            word_count += 1
            if word_count > words_to_return:
                result.append('...')
                break
        result.append(part)
    
    return ''.join(result)


@register.filter(name="reading_time")
def reading_time(value):
    """
    Estimates reading time for an article.
    
    Usage: {{ article.content|reading_time }}
    """
    if not value:
        return "0 min read"
    
    # Count words (roughly)
    word_count = len(value.split())
    
    # Average reading speed: 200 words per minute
    minutes = max(1, word_count // 200)
    
    if minutes == 1:
        return "1 min read"
    else:
        return f"{minutes} min read"
```

Update the article detail template to use our new filters. In `news/templates/news/article_detail.html`, add:

```html
{% load news_extras %}

<!-- Add under the article meta info -->
<div class="reading-time">
    {{ article.content|reading_time }}
</div>
```

Also, update the home template to use the truncate filter in `news/templates/news/home.html`:

```html
{% load news_extras %}

<!-- Replace the summary paragraph with -->
<p>{{ article.content|truncate_words_html:30 }}</p>
```

## Testing Your Application 🧪

To ensure our application works as expected, let's write some tests for our models and views.

### Writing Model Tests

Create tests in `news/tests.py`:

```python
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from .models import Category, Reporter, Article, Tag


class CategoryModelTest(TestCase):
    """Test cases for the Category model"""
    
    def test_category_creation(self):
        """Test creating a category and checking slug generation"""
        category = Category.objects.create(name="Technology")
        self.assertEqual(category.name, "Technology")
        self.assertEqual(category.slug, "technology")
        self.assertEqual(str(category), "Technology")


class ReporterModelTest(TestCase):
    """Test cases for the Reporter model"""
    
    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testuser",
            first_name="Test",
            last_name="User",
            email="test@example.com",
            password="testpassword"
        )
    
    def test_reporter_creation(self):
        """Test creating a reporter profile"""
        reporter = Reporter.objects.create(
            user=self.user,
            bio="Test reporter bio"
        )
        self.assertEqual(str(reporter), "Test User")
        self.assertEqual(reporter.bio, "Test reporter bio")


class ArticleModelTest(TestCase):
    """Test cases for the Article model"""
    
    def setUp(self):
        """Set up test data"""
        # Create user and reporter
        self.user = User.objects.create_user(
            username="reporter",
            first_name="Jane",
            last_name="Doe",
            password="password123"
        )
        self.reporter = Reporter.objects.create(user=self.user)
        
        # Create category
        self.category = Category.objects.create(name="Sports")
        
        # Create tags
        self.tag1 = Tag.objects.create(name="Football")
        self.tag2 = Tag.objects.create(name="World Cup")
    
    def test_article_creation(self):
        """Test creating an article with relationships"""
        article = Article.objects.create(
            title="Test Article",
            content="This is test content for the article.",
            reporter=self.reporter,
            category=self.category,
            status="published"
        )
        
        # Add tags
        article.tags.add(self.tag1, self.tag2)
        
        # Test basic properties
        self.assertEqual(article.title, "Test Article")
        self.assertEqual(article.slug, "test-article")
        self.assertEqual(str(article), "Test Article")
        
        # Test relationships
        self.assertEqual(article.reporter, self.reporter)
        self.assertEqual(article.category, self.category)
        self.assertEqual(article.tags.count(), 2)
        self.assertTrue(self.tag1 in article.tags.all())
        self.assertTrue(self.tag2 in article.tags.all())
        
        # Test summary generation
        self.assertTrue(article.summary.startswith("This is test content"))


class ArticleViewTests(TestCase):
    """Test cases for article views"""
    
    def setUp(self):
        """Set up test data"""
        # Create user and reporter
        self.user = User.objects.create_user(
            username="testuser", 
            password="testpass123"
        )
        self.reporter = Reporter.objects.create(user=self.user)
        
        # Create category
        self.category = Category.objects.create(
            name="Technology",
            description="Tech news and reviews"
        )
        
        # Create articles
        self.article1 = Article.objects.create(
            title="First Test Article",
            slug="first-test-article",
            content="This is the content of the first test article.",
            reporter=self.reporter,
            category=self.category,
            status="published"
        )
        
        self.article2 = Article.objects.create(
            title="Second Test Article",
            slug="second-test-article",
            content="This is the content of the second test article.",
            reporter=self.reporter,
            category=self.category,
            status="published"
        )
        
        # Create draft article
        self.draft_article = Article.objects.create(
            title="Draft Article",
            slug="draft-article",
            content="This is a draft article.",
            reporter=self.reporter,
            category=self.category,
            status="draft"
        )
    
    def test_home_view(self):
        """Test the home page view"""
        response = self.client.get(reverse("news:home"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/home.html")
        self.assertContains(response, "First Test Article")
        self.assertContains(response, "Second Test Article")
        self.assertNotContains(response, "Draft Article")  # Draft should not appear
    
    def test_article_detail_view(self):
        """Test the article detail view"""
        response = self.client.get(
            reverse("news:article_detail", args=[self.article1.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/article_detail.html")
        self.assertContains(response, "First Test Article")
        self.assertContains(response, "This is the content")
    
    def test_category_view(self):
        """Test the category detail view"""
        response = self.client.get(
            reverse("news:category_detail", args=[self.category.slug])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/category_detail.html")
        self.assertContains(response, "Technology")
        self.assertContains(response, "First Test Article")
        self.assertContains(response, "Second Test Article")


### Running Tests

Run the tests using:

```bash
python3 manage.py test news
```

You should see output like:

```
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
....
----------------------------------------------------------------------
Ran 4 tests in 0.123s

OK
Destroying test database for alias 'default'...
```

Now create a superuser to access the admin interface:

```bash
python3 manage.py createsuperuser
```

Follow the prompts to enter username, email, and password. Then run the development server:

```bash
python3 manage.py runserver
```

Now you can access the admin interface at http://127.0.0.1:8000/admin/ and log in with your superuser credentials. Add some categories, reporters, articles, and tags to see your news portal in action!

## Applications to Extend Functionality 💡

Our news portal can be extended with additional applications to enhance its functionality. Here are three potential extensions:

### 1. Comments App

A comments application would allow readers to engage with the content, providing feedback and starting discussions.

**Key Features:**
- Commenting on articles
- Threaded replies to comments
- Comment moderation by staff
- Upvoting/downvoting comments
- Email notifications for replies

**Basic Models:**
```python
class Comment(models.Model):
    article = models.ForeignKey('news.Article', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='replies')
    body = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    is_approved = models.BooleanField(default=False)
    upvotes = models.PositiveIntegerField(default=0)
    downvotes = models.PositiveIntegerField(default=0)
    
    def __str__(self):
        return f'Comment by {self.author.username} on {self.article.title}'
```

### 2. User Profiles App

A user profiles application would enhance user engagement by allowing readers to maintain profiles, save articles, and follow topics.

**Key Features:**
- Extended user profiles
- Article bookmarking
- Topic following
- Reading history
- User preferences (e.g., dark mode, email preferences)

**Basic Models:**
```python
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    bio = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    
    # Relationships
    bookmarked_articles = models.ManyToManyField('news.Article', blank=True, related_name='bookmarked_by')
    followed_categories = models.ManyToManyField('news.Category', blank=True, related_name='followers')
    followed_reporters = models.ManyToManyField('news.Reporter', blank=True, related_name='followers')
    
    # Preferences
    email_notifications = models.BooleanField(default=True)
    dark_mode = models.BooleanField(default=False)
    
    def __str__(self):
        return f'Profile for {self.user.username}'


class ReadingHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='reading_history')
    article = models.ForeignKey('news.Article', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    read_completion = models.FloatField(default=0.0)  # 0.0 to 1.0 indicating reading progress
    
    class Meta:
        unique_together = ('user', 'article')
        ordering = ['-timestamp']
    
    def __str__(self):
        return f'{self.user.username} read {self.article.title}'
```

### 3. Newsletter App

A newsletter application would help retain readers by sending regular updates about new content and trending topics.

**Key Features:**
- Email subscription management
- Automated newsletter generation
- Category-specific newsletters
- Click tracking and analytics
- Custom newsletter templates

**Basic Models:**
```python
class Subscriber(models.Model):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100, blank=True)
    is_active = models.BooleanField(default=True)
    confirmed = models.BooleanField(default=False)
    confirmation_token = models.CharField(max_length=100, blank=True)
    date_subscribed = models.DateTimeField(auto_now_add=True)
    
    # Subscription preferences
    subscribed_categories = models.ManyToManyField('news.Category', blank=True)
    daily_digest = models.BooleanField(default=False)
    weekly_digest = models.BooleanField(default=True)
    
    def __str__(self):
        return self.email


class Newsletter(models.Model):
    FREQUENCY_CHOICES = (
        ('daily', 'Daily'),
        ('weekly', 'Weekly'),
        ('monthly', 'Monthly'),
        ('special', 'Special Edition'),
    )
    
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    frequency = models.CharField(max_length=10, choices=FREQUENCY_CHOICES)
    template = models.TextField(help_text="HTML template with placeholders")
    created_date = models.DateTimeField(auto_now_add=True)
    sent_date = models.DateTimeField(null=True, blank=True)
    
    # Content selections
    featured_articles = models.ManyToManyField('news.Article', related_name='featured_in_newsletters')
    categories = models.ManyToManyField('news.Category', blank=True)
    
    def __str__(self):
        return f'{self.title} ({self.get_frequency_display()})'


class NewsletterDelivery(models.Model):
    newsletter = models.ForeignKey(Newsletter, on_delete=models.CASCADE)
    subscriber = models.ForeignKey(Subscriber, on_delete=models.CASCADE)
    sent_at = models.DateTimeField(auto_now_add=True)
    opened = models.BooleanField(default=False)
    open_date = models.DateTimeField(null=True, blank=True)
    click_count = models.PositiveIntegerField(default=0)
    
    class Meta:
        unique_together = ('newsletter', 'subscriber')
    
    def __str__(self):
        return f'{self.newsletter} sent to {self.subscriber.email}'
```

## Next Steps 🚶

After completing this guide, you've built a solid foundation for your news portal. Here are some suggested next steps to enhance your application:

1. **Improve Design and UI**
   - Implement a proper CSS framework like Bootstrap or Tailwind
   - Add responsive design for mobile devices
   - Create a more engaging homepage with featured articles
   - Implement dark mode using CSS variables

2. **Performance Optimization**
   - Add caching for frequently accessed pages
   - Implement database query optimization
   - Use Django's select_related and prefetch_related for related objects
   - Add pagination for large result sets

3. **Search Functionality**
   - Add a search form to the navigation bar
   - Implement basic search by title and content
   - Consider using django-watson or django-haystack for advanced search
   - Add filters for searching by category, date, or reporter

4. **User Authentication and Permissions**
   - Implement social authentication (Google, Facebook, etc.)
   - Add user roles (admin, editor, reporter, reader)
   - Create permission checks for content editing
   - Add staff-only sections in the frontend

5. **Content Enhancement**
   - Add rich text editing with a WYSIWYG editor
   - Implement media library for images and videos
   - Add support for embedding content (YouTube, Twitter, etc.)
   - Implement scheduled publishing for articles

6. **SEO Improvements**
   - Add meta tags for title, description, and keywords
   - Implement Open Graph tags for social sharing
   - Create XML sitemaps for search engines
   - Implement canonical URLs and structured data

7. **Analytics and Metrics**
   - Track page views and popular articles
   - Measure reading time and engagement
   - Create a dashboard for editors to view metrics
   - Implement A/B testing for headlines

8. **Deploy Your Application**
   - Set up a production environment
   - Configure a web server (Nginx, Apache)
   - Set up HTTPS with Let's Encrypt
   - Implement proper security measures

This news portal demonstrates Django's capabilities for building content-driven applications. The skills you've learned—template inheritance, admin customization, and building dynamic views—will be valuable for many other types of web applications.

By extending the project with the suggested applications and improvements, you can create a comprehensive platform that not only delivers news but also engages readers and builds a community around your content.
