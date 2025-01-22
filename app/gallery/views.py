from django.views.generic import TemplateView

# Create your views here.
class GalleryView(TemplateView):
    template_name = 'gallery.html'