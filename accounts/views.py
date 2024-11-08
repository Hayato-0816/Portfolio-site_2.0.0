from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm

class LoginView(LoginView):
    template_name = 'accounts/login.html'  # テンプレートのパスを明示的に指定
    redirect_authenticated_user = True  # すでにログインしているユーザーをリダイレクト
    
    def get_success_url(self):
        return reverse_lazy('accounts:dashboard')  # ログイン後のリダイレクト先

class SignupView(TemplateView):
    template_name = 'accounts/signup.html'

class PasswordResetView(TemplateView):
    template_name = 'accounts/password_reset.html'

class DashboardView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'accounts/dashboard.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = CategoryForm()
        return context

    def post(self, request, *args, **kwargs):
        # object_listを設定
        self.object_list = self.get_queryset()
        
        if 'logout' in request.POST:
            logout(request)
            return redirect('accounts:login')

        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('blog:home')

        if 'delete_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = get_object_or_404(Category, id=category_id)
            category.delete()
            return redirect('blog:home')

        # フォームが無効な場合
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)
    
    def logout(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
            return redirect('accounts:login')
        return super().post(request, *args, **kwargs)

        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = CategoryForm()  # フォームをコンテキストに追加
        return context