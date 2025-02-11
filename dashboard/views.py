from django.views.generic import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
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
    
    def get(self, request, *args, **kwargs):
        if kwargs.get('action') == 'get_about_item':
            return self.get_about_item(request, kwargs.get('type'), kwargs.get('pk'))

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

    def post(self, request, *args, **kwargs):
        # 更新処理の場合
        if kwargs.get('action') == 'update_about_item':
            return self.update_about_item(request, kwargs.get('type'), kwargs.get('pk'))
        # 削除処理の場合
        if kwargs.get('action') == 'delete_about_item':
            return self.delete_about_item(request, kwargs.get('type'), kwargs.get('pk'))
        
        # 新規作成処理
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
    
    def get_about_item(self, request, type, pk):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                # タイプに応じてモデルを選択
                if type == 'main':
                    item = get_object_or_404(AboutMainCategory, pk=pk)
                    response_data = {
                        'id': item.id,
                        'name': item.name,
                        'type': type,
                        'is_active': item.is_active,
                        'order': item.order
                    }
                elif type == 'sub':
                    item = get_object_or_404(AboutSubCategory, pk=pk)
                    response_data = {
                        'id': item.id,
                        'name': item.name,
                        'type': type,
                        'is_active': item.is_active,
                        'main_category_id': item.main_category.id,
                        'main_category_name': item.main_category.name,
                        'order': item.order
                    }
                elif type == 'skill':
                    item = get_object_or_404(AboutSkill, pk=pk)
                    response_data = {
                        'id': item.id,
                        'name': item.name,
                        'type': type,
                        'is_active': item.is_active,
                        'sub_category_id': item.sub_category.id,
                        'sub_category_name': item.sub_category.name,
                        'order': item.order
                    }
                else:
                    return JsonResponse({'error': '不正なタイプです'}, status=400)

                # オブジェクトのデータをJSONで返す
                return JsonResponse({
                    'status': 'success',
                    'item': response_data
                })
            except Exception as e:
                return JsonResponse({'error': str(e)}, status=500)
        return JsonResponse({'error': '不正なリクエストです'}, status=400)
    
    def update_about_item(self, request, type, pk):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                if type == 'main':
                    item = get_object_or_404(AboutMainCategory, pk=pk)
                    form = AboutMainCategoryForm(request.POST, instance=item)
                elif type == 'sub':
                    item = get_object_or_404(AboutSubCategory, pk=pk)
                    # メインカテゴリーの値を分割
                    main_category_value = request.POST.get('main_category', '')
                    main_category_id = main_category_value.split(':')[0]
                    
                    # POSTデータを更新
                    post_data = request.POST.copy()
                    post_data['main_category'] = main_category_id
                    form = AboutSubCategoryForm(post_data, instance=item)
                elif type == 'skill':
                    item = get_object_or_404(AboutSkill, pk=pk)
                    # サブカテゴリーの値を分割
                    sub_category_value = request.POST.get('sub_category', '')
                    sub_category_id = sub_category_value.split(':')[0]
                    
                    # POSTデータを更新
                    post_data = request.POST.copy()
                    post_data['sub_category'] = sub_category_id  # IDのみを設定
                    form = AboutSkillForm(post_data, instance=item)
                else:
                    return JsonResponse({'status': 'error', 'errors': '不正なタイプです'})

                if form.is_valid():
                    item = form.save()
                    if type == 'main':
                        response_data = {
                            'id': item.id,
                            'name': item.name,
                            'type': type,
                            'is_active': item.is_active,
                            'order': item.order
                        }
                    elif type == 'sub':
                        response_data = {
                            'id': item.id,
                            'name': item.name,
                            'type': type,
                            'is_active': item.is_active,
                            'main_category_id': item.main_category.id,
                            'main_category_name': item.main_category.name,
                            'order': item.order
                        }
                    elif type == 'skill':
                        response_data = {
                            'id': item.id,
                            'name': item.name,
                            'type': type,
                            'is_active': item.is_active,
                            'sub_category_id': item.sub_category.id,
                            'sub_category_name': item.sub_category.name,
                            'order': item.order
                        }
                    
                    return JsonResponse({
                        'status': 'success',
                        'item': response_data
                    })
                    
                return JsonResponse({'status': 'error', 'errors': form.errors})
            except Exception as e:
                return JsonResponse({'status': 'error', 'errors': str(e)})
        return JsonResponse({'status': 'error', 'errors': '不正なリクエストです'})

    def delete_about_item(self, request, type, pk):
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            try:
                if type == 'main':
                    item = get_object_or_404(AboutMainCategory, pk=pk)
                elif type == 'sub':
                    item = get_object_or_404(AboutSubCategory, pk=pk)
                elif type == 'skill':
                    item = get_object_or_404(AboutSkill, pk=pk)
                else:
                    return JsonResponse({'status': 'error', 'message': '不正なタイプです'})
                
                item.delete()
                return JsonResponse({'status': 'success'})
            except Exception as e:
                return JsonResponse({'status': 'error', 'message': str(e)})
        return JsonResponse({'status': 'error', 'message': '不正なリクエストです'})


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
