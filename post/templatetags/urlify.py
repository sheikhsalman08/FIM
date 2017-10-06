from django import template 

register = template.Library()

@register.filter('urlify')
def urlify(value):
    return value+1