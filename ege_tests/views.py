from django.views.generic import TemplateView


class Homepage(TemplateView):
    """Отображение главной страницы"""
    template_name = 'homepage.html'
