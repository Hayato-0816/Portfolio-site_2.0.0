from django.views.generic import *
from .models import *
from django.urls import reverse_lazy

class MessageView(CreateView):
    model = Message
    template_name = 'contact.html'
    fields = ['company_name', 'name', 'email', 'phone_number', 'category', 'message']
    # success_url = reverse_lazy('contact_success')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
