from django.views.generic import *
from .models import *

# Category ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class CategoryListView(ListView):
    model = Category
    template_name = 'blog/category.html'

# Post List ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class PostListView(ListView):
    model = Post
    template_name = 'blog/blog.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

    def get_queryset(self):
        return Post.objects.filter(status='published')

# Post Detail ///////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'

    def get_queryset(self):
        return Post.objects
    