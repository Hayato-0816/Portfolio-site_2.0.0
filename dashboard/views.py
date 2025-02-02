from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect
from .forms import AboutMainCategoryForm, AboutSubCategoryForm, AboutSkillForm
from app.blog.models import *
from app.about.models import *


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
        return BlogPost.objects.filter(author=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        # context['form'] = CategoryForm()
        context['is_dashboard'] = True
        return context

    def post(self, request, *args, **kwargs):
        # object_listを設定
        self.object_list = self.get_queryset()
        
        if 'logout' in request.POST:
            logout(request)
            return redirect('dashboard:login')

        # form = CategoryForm(request.POST)
        # if form.is_valid():
        #     form.save()
        #     return redirect('blog:home')

        # if 'delete_category' in request.POST:
        #     category_id = request.POST.get('category_id')
        #     category = get_object_or_404(BlogCategory, id=category_id)
        #     category.delete()
        #     return redirect('blog:home')

        # # フォームが無効な場合
        # context = self.get_context_data()
        # context['form'] = form
        # return render(request, self.template_name, context)
    
    def logout(self, request, *args, **kwargs):
        if 'logout' in request.POST:
            logout(request)
            return redirect('dashboard:login')
        return super().post(request, *args, **kwargs)

class AboutView(LoginRequiredMixin,FormView):
    template_name = 'dashboard/about/about.html'
    login_url = reverse_lazy('dashboard:login')
    raise_exception = False
    form_class = AboutMainCategoryForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['about_data'] = {
            'main_categories': AboutMainCategory.objects.all(),
            'sub_categories': AboutSubCategory.objects.all(),
            'skills': AboutSkill.objects.all(),
        }
        
        return context

class BlogView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/blog/blog.html'
    login_url = reverse_lazy('dashboard:login')
    raise_exception = False

class BlogCategoryListView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/blog/category_edit.html'
    login_url = reverse_lazy('dashboard:login')
    raise_exception = False

class GalleryView(LoginRequiredMixin,TemplateView):
    template_name = 'dashboard/gallery/gallery.html'
    login_url = reverse_lazy('dashboard:login')
    raise_exception = False
