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