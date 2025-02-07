from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect, render
from django.http import JsonResponse
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

class AboutView(LoginRequiredMixin,TemplateView):
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

    def post(self, request):
        form_type = request.POST.get('form_type')
        
        if form_type == 'main_category':
            form = AboutMainCategoryForm(request.POST)
        elif form_type == 'sub_category':
            form = AboutSubCategoryForm(request.POST)
        elif form_type == 'skill':
            form = AboutSkillForm(request.POST)
        else:
            return JsonResponse({'status': 'error', 'message': '不正なフォームタイプです'})

        if form.is_valid():
            form.save()
            return JsonResponse({'status': 'success'})
        
        return JsonResponse({
            'status': 'error',
            'errors': form.errors
        })
    
        def get_about_item(request, type, pk):
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                try:
                    # タイプに応じてモデルを選択
                    if type == 'main':
                        item = get_object_or_404(AboutMainCategory, pk=pk)
                    elif type == 'sub':
                        item = get_object_or_404(AboutSubCategory, pk=pk)
                    elif type == 'skill':
                        item = get_object_or_404(AboutSkill, pk=pk)
                    else:
                        return JsonResponse({'error': '不正なタイプです'}, status=400)

                    # オブジェクトのデータをJSONで返す
                    return JsonResponse({
                        'status': 'success',
                        'item': {
                            'id': item.id,
                            'name': item.name,
                            'type': type
                        }
                    })
                except Exception as e:
                    return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'error': '不正なリクエストです'}, status=400)
    


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
