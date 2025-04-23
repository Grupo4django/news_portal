from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Comment
from news.models import Article
from .forms import CommentForm

@login_required
def add_comment(request, article_id):
    article = get_object_or_404(Article, id=article_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.article = article
            comment.author = request.user
            comment.save()
            return redirect('news:article_detail', pk=article_id)
    return redirect('news:article_detail', pk=article_id)

@login_required
def reply_comment(request, comment_id):
    parent_comment = get_object_or_404(Comment, id=comment_id)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            reply = form.save(commit=False)
            reply.article = parent_comment.article
            reply.author = request.user
            reply.parent = parent_comment
            reply.save()
    return redirect('news:article_detail', pk=parent_comment.article.id)

@login_required
@require_POST
def vote_comment(request, comment_id, vote_type):
    comment = get_object_or_404(Comment, id=comment_id)
    if vote_type == 'up':
        comment.upvotes += 1
    elif vote_type == 'down':
        comment.downvotes += 1
    comment.save()
    return JsonResponse({
        'upvotes': comment.upvotes,
        'downvotes': comment.downvotes
    })
