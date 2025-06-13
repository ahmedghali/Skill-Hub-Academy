from django import template

register = template.Library()

@register.filter
def multiply_stars(value, char):
    """Répète un caractère (par exemple, '★') un certain nombre de fois."""
    try:
        return char * int(value)
    except (ValueError, TypeError):
        return ''

@register.filter
def subtract(value, arg):
    """Soustrait arg de value."""
    try:
        return int(value) - int(arg)
    except (ValueError, TypeError):
        return 0