from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def highlight(text, word):
    if word:
        return mark_safe(text.replace(word, "<span class='highlight'>%s</span>" % word))
    else:
        return text
