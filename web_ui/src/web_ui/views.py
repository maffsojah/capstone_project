from django.views import generic


class HomePage(generic.TemplateView):
    template_name = "home.html"

class ServicesPage(generic.TemplateView):
    template_name = "services.html"

class AboutPage(generic.TemplateView):
    template_name = "about.html"
