from django import template

register = template.Library()




@register.filter
def get_value(value, arg):
    return value.get(arg)