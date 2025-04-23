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