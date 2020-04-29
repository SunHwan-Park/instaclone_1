from django.shortcuts import render, redirect, get_object_or_404
from .models import Article
from .forms import ArticleForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
import random

User = get_user_model()


@login_required
def index(request):
    users = User.objects.all() # 전체 유저 그룹
    followings = request.user.followings.all() # 사용자가 팔로잉하고 있는 유저 그룹
    unfollowings = users.difference(followings) # 사용자가 팔로잉하고 있지 않은 유저 그룹
    if len(unfollowings) >= 5: # 만약 그 수가 5 이상이라면
        # 랜덤하게 5명만 뽑아 추천.
        # queryset은 random.shufle()이 먹히지 않는다. 따라서 아래와 같이 구현해야한다.
        # unfollowings = sorted(unfollowings, key=lambda x: random.random())[:5]
        # 서로 많은 친구(내가 팔로잉하고 있는 유저)를 공유하고 있는 사람 5명 뽑아 추천
        unfollowings = sorted(unfollowings, reverse=True, key=lambda x: x.followings.all().intersection(request.user.followings.all()).count())[:5]

    articles = [] # 넘겨줄 글 목록
    for following in followings: # 팔로잉 하고 있는 유저
        for article in following.article_set.all(): # 해당 유저가 쓴 글
            articles.append(article)
    # 해당 글들 생성시간 순으로 정렬
    articles = sorted(articles, key=lambda article: article.created_at)

    context = {
        'unfollowings': unfollowings,
        'articles': articles,
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