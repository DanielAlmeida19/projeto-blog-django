from django.core.paginator import Paginator
from django.shortcuts import render
from blog.models import Post, Page, Tag
from django.db.models import Q
from django.contrib.auth.models import User
from django.http import Http404

PER_PAGE = 9


def index(request):
    posts = (
        Post.objects.get_published()
    )
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': 'Home - '
        }
    )


def page(request, slug):

    req_page = (
        Page.objects
        .filter(is_published=True)
        .filter(slug=slug)
        .first()
    )

    if req_page is None:
        raise Http404()

    page_title = f'{req_page.title} - Página - '

    return render(
        request,
        'blog/pages/page.html',
        {
            'page': req_page,
            'page_title': page_title
        }
    )


def post(request, slug):

    post = (
        Post.objects.get_published()
        .filter(slug=slug)
        .first()
    )

    if post is None:
        raise Http404()

    page_title = f'{post.title} - Post - '

    return render(
        request,
        'blog/pages/post.html',
        {
            'post': post,
            'page_title': page_title
        }
    )


def created_by(request, author_pk):

    user = User.objects.filter(pk=author_pk).first()

    if user is None:
        raise Http404()

    user_full_name = user.username

    if user.first_name:
        user_full_name = f'{user.first_name} {user.last_name}'

    posts = (
        Post.objects.get_published()
        .filter(created_by__pk=author_pk)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': f'{user_full_name} - '
        }
    )


def category(request, slug):
    posts = (
        Post.objects.get_published()
        .filter(category__slug=slug)
    )

    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    if len(page_obj) == 0:
        raise Http404()

    page_title = f'{page_obj[0].category.name} - Categoria - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title
        }
    )


def tag(request, slug):
    posts = (
        Post.objects.get_published()
        .filter(tags__slug=slug)
    )
    paginator = Paginator(posts, PER_PAGE)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)

    tag = Tag.objects.filter(slug=slug).first()

    if tag is None:
        raise Http404()

    page_title = f'{tag.name} - Tag - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': page_obj,
            'page_title': page_title
        }
    )


def search(request):
    search_value = request.GET.get('search', '').strip()
    posts = (
        Post.objects.get_published()
        .filter(
            # Título contém search_value OU
            Q(title__icontains=search_value) |
            # Título contém search_value OU
            Q(excerpt__icontains=search_value) |
            # Conteúdo contém search_value
            Q(content__icontains=search_value)
        )[0:PER_PAGE]
    )

    page_title = f'{search_value[:30]} - '

    return render(
        request,
        'blog/pages/index.html',
        {
            'page_obj': posts,
            'search_value': search_value,
            'page_title': page_title
        }
    )
