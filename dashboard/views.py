from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import *
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.shortcuts import render, redirect, get_object_or_404
from .forms import CategoryForm
from about.models import MainCategory, SubCategory, Skill  # aboutアプリのモデルをインポート

class LoginView(LoginView):
    template_name = 'authentication/login.html'  # テンプレートのパスを明示的に指定
    redirect_authenticated_user = True  # すでにログインしているユーザーをリダイレクト
    
    def get_success_url(self):
        return reverse_lazy('dashboard:dashboard')  # ログイン後のリダイレクト先

class SignupView(TemplateView):
    template_name = 'authentication/signup.html'

class PasswordResetView(TemplateView):
    template_name = 'authentication/password_reset.html'

class DashboardView(LoginRequiredMixin, ListView):
    template_name = 'dashboard/dashboard.html'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['form'] = CategoryForm()
        context['is_dashboard'] = True
        return context

    def post(self, request, *args, **kwargs):
        # object_listを設定
        self.object_list = self.get_queryset()
        
        if 'logout' in request.POST:
            logout(request)
            return redirect('dashboard:login')

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
            return redirect('dashboard:login')
        return super().post(request, *args, **kwargs)

class AboutView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/about/about.html'
    login_url = reverse_lazy('dashboard:login')
    raise_exception = False

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 各モデルのデータを個別に取得
        context['main_categories'] = MainCategory.objects.filter(
            is_active=True
        ).order_by('order')
        
        context['sub_categories'] = SubCategory.objects.filter(
            is_active=True
        ).order_by('main_category', 'order')
        
        context['skills'] = Skill.objects.filter(
            is_active=True
        ).order_by('sub_category', 'order')
        
        return context
        
class BlogView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/blog/blog.html'
    login_url = reverse_lazy('dashboard:login')
    raise_exception = False

class GalleryView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/gallery/gallery.html'
    login_url = reverse_lazy('dashboard:login')
    raise_exception = False
