from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model

User = get_user_model()


@login_required
def index(request):
    users = User.objects.all()
    followings = request.user.followings.all()
    unfollowings = users.difference(followings)
    articles = []
    for following in followings:
        for article in following.article_set.all():
            articles.append(article)
    articles.sort(key=lambda article: article.created_at)
    context = {
        'articles': articles,
        'unfollowings': unfollowings,
    }
    return render(request, 'articles/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            form.save_m2m()
            return redirect('profile', request.user.username)
    else:
        form = ArticleForm()
    context = {
        'form': form,
    }
    return render(request, 'articles/form.html', context)

@login_required
def like_root(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user
    if request.user in article.like_users.all():
        article.like_users.remove(user)
    else:
        article.like_users.add(user)
    return redirect('root')

@login_required
def like_profile(request, article_pk):
    article = get_object_or_404(Article, pk=article_pk)
    user = request.user
    if request.user in article.like_users.all():
        article.like_users.remove(user)
    else:
        article.like_users.add(user)
    return redirect('profile', article.user.username)

@login_required
def tag_search(request, tag_name):
    tag_articles = Article.objects.filter(tags__name__in=[tag_name]).distinct()

    context = {
        'tag_articles':tag_articles,
        'tag_name':tag_name,
    }
    return render(request, 'articles/tag_articles.html', context)