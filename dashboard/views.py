from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from .forms import AboutMainCategoryForm, AboutSubCategoryForm, AboutSkillForm
from app.about.models import *
from app.blog.models import *


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

class AboutView(LoginRequiredMixin, View):  # FormViewからViewに変更
    template_name = 'dashboard/about/about.html'
    login_url = reverse_lazy('dashboard:login')
    raise_exception = False
    
    def get(self, request):
        main_category_form = AboutMainCategoryForm()
        sub_category_form = AboutSubCategoryForm()
        skill_form = AboutSkillForm()
        
        context = {
            'about_data': {
                'main_categories': AboutMainCategory.objects.all(),
                'sub_categories': AboutSubCategory.objects.all(),
                'skills': AboutSkill.objects.all(),
            },
            'main_category_form': main_category_form,
            'sub_category_form': sub_category_form,
            'skill_form': skill_form
        }
        return render(request, self.template_name, context)

    def create_about_data(self, request):
        main_category_form = AboutMainCategoryForm(request.POST)
        sub_category_form = AboutSubCategoryForm(request.POST)
        skill_form = AboutSkillForm(request.POST)
        
        if main_category_form.is_valid():
            main_category_form.save()
            return redirect('dashboard:about')
        
        if sub_category_form.is_valid():
            sub_category_form.save()
            return redirect('dashboard:about')
        
        if skill_form.is_valid():
            skill_form.save()
            return redirect('dashboard:about')
        
        # フォームが無効な場合、エラーを含めて再表示
        context = {
            'about_data': {
                'main_categories': AboutMainCategory.objects.all(),
                'sub_categories': AboutSubCategory.objects.all(),
                'skills': AboutSkill.objects.all(),
            },
            'main_category_form': main_category_form,
            'sub_category_form': sub_category_form,
            'skill_form': skill_form
        }
        return render(request, self.template_name, context)
    


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
