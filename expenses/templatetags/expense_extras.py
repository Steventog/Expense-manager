from django import template
from decimal import Decimal

register = template.Library()

@register.filter
def subtract(value, arg):
    """Soustrait arg de value"""
    try:
        return value - arg
    except (ValueError, TypeError):
        return value

@register.filter
def percentage_used(value, total):
    """
    Calcule le pourcentage utilisé (100 - pourcentage restant)
    """
    try:
        value = float(value)
        total = float(total)
        if total == 0:
            return 100
        return 100 - ((value / total) * 100)
    except (ValueError, TypeError):
        return 0
