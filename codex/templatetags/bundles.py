from django import template

register = template.Library()

@register.filter
def cap(s):
    return s[0].upper()+s[1:]
