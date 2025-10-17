from django import template
from django.utils.formats import number_format

register = template.Library()

@register.filter
def currency(value, currency_code='IDR'):
    """
    Format a number as currency
    """
    try:
        value = float(value)
        formatted_value = number_format(value, decimal_pos=0, force_grouping=True)
        if currency_code == 'IDR':
            return f'Rp{formatted_value}'
        return f'{currency_code} {formatted_value}'
    except (ValueError, TypeError):
        return value