from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm, PostForm


# Account Managements ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class LoginView(LoginView):
    template_name = 'dashboard/login.html'  # テンプレートのパスを明示的に指定
    redirect_authenticated_user = True  # すでにログインしているユーザーをリダイレクト
    
    def get_success_url(self):
        return reverse_lazy('dashboard:blog_management')  # ログイン後のリダイレクト先

class SignupView(TemplateView):
    template_name = 'dashboard/signup.html'

class PasswordResetView(TemplateView):
    template_name = 'dashboard/password_reset.html'

# Dashboard ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

# Blog ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class BlogmanagementView(LoginRequiredMixin, ListView):
    # 基本設定
    model = Post
    template_name = 'dashboard/blog_management.html'
    context_object_name = 'posts'
    paginate_by = 10

    # 1. クエリセットの取得
    def get_queryset(self):
        # ログインユーザーの投稿のみを取得
        return Post.objects.filter(author=self.request.user)

    # 3. POSTリクエストの処理
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        
        # ログアウト処理
        if 'logout' in request.POST:
            logout(request)
            return redirect('dashboard:login')

class CategoryDetailView(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'dashboard/category_detail.html'
    context_object_name = 'category'

    # 1. コンテキストデータの取得（重複している - 要修正）
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # すべてのカテゴリーを取得
        context['form'] = CategoryForm()  # カテゴリー作成フォーム
        return context

    # 2. POSTリクエストの処理
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()

        # カテゴリー作成処理
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('dashboard:blog_management')
        
        # カテゴリー更新処理
        if 'update_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                return redirect('dashboard:blog_management')

        # カテゴリー削除処理
        if 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return redirect('dashboard:blog_management')

        # フォームが無効な場合の処理
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

class PostDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'dashboard/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()  # カテゴリー選択用
                # フォームを初期化して追加
        if 'form' not in context:
            context['form'] = PostForm(instance=self.object)
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()  # 現在の投稿を取得
        form = None

        # 投稿更新処理
        if 'update_post' in request.POST:
            form = PostForm(request.POST, request.FILES, instance=self.object)
            if form.is_valid():
                post = form.save(commit=False)
                post.author = request.user  # 著者を設定
                post.save()
                return redirect('dashboard:blog_management')

        # 投稿削除処理
        if 'delete_post' in request.POST:
            self.object.delete()
            return redirect('dashboard:blog_management')
        
        if form is None:
            form = PostForm(instance=self.object)

        # フォームが無効な場合
        return self.render_to_response(self.get_context_data(form=form))

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'dashboard/post_create.html'
    form_class = PostForm
    success_url = reverse_lazy('dashboard:blog_management')

    def form_valid(self, form):
        # 保存前に現在のユーザーを著者として設定
        form.instance.author = self.request.user
        return super().form_valid(form)