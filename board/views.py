from datetime import datetime
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.core.mail import send_mail
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Article, UserResponse
from .forms import ArticleForm, ResponseForm
from django.contrib.auth.mixins import LoginRequiredMixin


class ArticleList(ListView):
    model = Article
    ordering = '-dateCreation'
    template_name = 'flatpages/articles.html'
    context_object_name = 'articles'
    paginate_by = 6
    media = 'uploads'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class ArticleDetail(DetailView):
    model = Article
    template_name = 'flatpages/article.html'
    context_object_name = 'article'
    media = 'uploads'


class ArticleCreate(LoginRequiredMixin, CreateView):
    permission_required = ('board.add_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'flatpages/article_create.html'
    media = 'uploads'

    def form_valid(self, form):
        article = form.save(commit=False)
        article.author = self.request.user
        article.save()
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, UpdateView):
    permission_required = ('board.update_article',)
    raise_exception = True
    form_class = ArticleForm
    model = Article
    template_name = 'flatpages/article_update.html'
    media = 'uploads'

    def image_update(request):
        if request.method == 'POST':
            form = ArticleForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                img_obj = form.instance
                return render(request, 'articles.html', {'form': form, 'img_obj': img_obj})
        else:
            form = ArticleForm()
        return render(request, 'article.html', {'form': form})


class ArticleDelete(LoginRequiredMixin, DeleteView):
    permission_required = ('articles.delete_article',)
    model = Article
    template_name = 'flatpages/article_delete.html'
    success_url = reverse_lazy('article_list')
    media = 'uploads'


class MyArticles(LoginRequiredMixin, ListView):
    permission_required = ('board.view_article',)
    model = Article
    ordering = '-dateCreation'
    template_name = 'flatpages/my_articles.html'
    context_object_name = 'MyArticles'
    paginate_by = 5

    def get_queryset(self):
        return Article.objects.filter(author=self.request.user)


class ResponseList(LoginRequiredMixin, ListView):
    permission_required = ('response.list_response',)
    model = UserResponse
    ordering = '-dateCreation'
    template_name = 'flatpages/response_list.html'
    context_object_name = 'responses'
    paginate_by = 6

    def get_queryset(self):
        return UserResponse.objects.filter(article__author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_now'] = datetime.utcnow()
        return context


class ResponseCreate(LoginRequiredMixin, CreateView):
    permission_required = ('response.add_response',)
    form_class = ResponseForm
    model = UserResponse
    template_name = 'flatpages/response.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        response = form.save(commit=False)
        response.author = self.request.user
        response.save()
        return super().form_valid(form)


class MyResponsesView(ListView):
    model = UserResponse
    form_class = ResponseForm
    template_name = 'flatpages/my_responses.html'
    context_object_name = 'responses'

    def get_queryset(self):
        queryset = super().get_queryset().filter(article__author=self.request.user)
        article_id = self.request.GET.get('responses')
        if article_id:
            queryset = queryset.filter(article_id=article_id)
        return queryset


def my_responses(request):
    user = request.user
    if request.method == 'POST':
        if 'accept_response' in request.POST:
            response_id = request.POST.get('accept_response')
            response = UserResponse.objects.get(pk=response_id)
            response.save()

        if 'delete_response' in request.POST:
            response_id = request.POST.get('delete_response')
            response = UserResponse.objects.get(pk=response_id)
            response.delete()

    responses = UserResponse.objects.filter(article__author=user)
    articles = Article.objects.filter(author=user)
    return render(request, 'my_responses.html', {'responses': responses, 'articles': articles})


def delete_responses(request, pk):
    response = get_object_or_404(UserResponse, pk=pk)
    if response.article.author == request.user:
        response.delete()
        send_mail(
            subject='На Ваш отклик отреагировали',
            message=f'Ваш отклик "{response.text}" к "{response.article.title}" был удалён',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.author.email],)

    return redirect('my_responses')


def accept_responses(request, pk):
    response = get_object_or_404(UserResponse, pk=pk)
    if response.article.author == request.user:
        article = response.article
        response.is_accepted = True
        response.save()
        article.save()
        send_mail(
            subject='На Ваш отклик отреагировали',
            message=f'Ваш отклик "{response.text}" к "{response.article.title}" был принят',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[response.author.email],
        )

    return redirect('my_responses')


















