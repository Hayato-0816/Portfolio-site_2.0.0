from django.views.generic import TemplateView
from .models import *

# Create your views here.
class AboutView(TemplateView):
    template_name = 'about.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_categories'] = AboutMainCategory.objects.filter(
            is_active=True
        ).prefetch_related(
            'sub_categories',
            'sub_categories__skills'
        )
        return context