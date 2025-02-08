from django import forms
from django.utils.safestring import mark_safe
from ..models import Tag

class HideListenTagWidget(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, renderer=None):
        all_tags = Tag.objects.all()
        if value is None:
            value = []
        hidden_tags = [tag for tag in all_tags if tag.code in ['listen', 'key'] and tag.pk in value]
        visible_tags = [tag for tag in all_tags if tag.code not in ['listen', 'key']]
        
        self.choices = [(tag.pk, tag.name) for tag in visible_tags]
        visible_output = super().render(name, value, attrs, renderer)

        hidden_output = ''
        if hidden_tags:
            for tag in hidden_tags:
                hidden_output += f'<input type="hidden" name="{name}" value="{tag.pk}" />'

        return mark_safe(visible_output + hidden_output)
