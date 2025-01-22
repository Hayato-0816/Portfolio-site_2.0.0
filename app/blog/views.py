from django.views.generic import *
from .models import *
from django.shortcuts import render
from django.db.models import Q

# Post List ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class PostListView(ListView):
    model = BlogPost
    template_name = 'blog.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BlogCategory.objects.all()
        return context

    def get_queryset(self):
        return BlogPost.objects.filter(status='published')

# Category ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class CategoryListView(ListView):
    model = BlogCategory
    template_name = 'category.html'

# Post Detail ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'post_detail.html'

    def get_queryset(self):
        return BlogPost.objects

def SearchView(request):
    query = request.GET.get('q', '')
    
    if query:
        results = BlogPost.objects.filter(
            Q(title__icontains=query) |
            Q(content__icontains=query)
        ).filter(status='published')  # 公開済みの記事のみを検索
        
        print(f"検索クエリ: {query}")  # デバッグ用
        print(f"検索結果数: {results.count()}")  # デバッグ用
    else:
        results = []
        
    return render(request, 'search.html', {
        'query': query,
        'results': results
    })