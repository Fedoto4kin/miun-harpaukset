from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'index.html'


class LexiconView(TemplateView):
    template_name = 'lexicon.html'

    def get_context_data(self, **kwargs):
        context = super(LexiconView, self).get_context_data(**kwargs)
        context['lexicon'] = True
        return context


class LessonsView(TemplateView):
    template_name = 'lessons.html'

    def get_context_data(self, **kwargs):
        context = super(LessonsView, self).get_context_data(**kwargs)
        context['lessons'] = True
        return context
