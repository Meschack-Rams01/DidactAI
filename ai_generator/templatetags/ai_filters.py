from django import template

register = template.Library()

@register.filter  
def to_letter(value):
    """
    Convert a number to a letter (1=A, 2=B, 3=C, etc.)
    More user-friendly than chr filter.
    """
    try:
        num = int(value)
        if 1 <= num <= 26:
            return chr(64 + num)  # A=65, B=66, etc.
        return str(num)
    except (ValueError, TypeError):
        return ''

@register.filter
def option_letter(value):
    """
    Convert option number to letter for multiple choice questions.
    1 -> A, 2 -> B, 3 -> C, 4 -> D, etc.
    """
    try:
        num = int(value)
        return chr(64 + num)  # 65 is ASCII for 'A'
    except (ValueError, TypeError):
        return str(value)

@register.filter(name='chr')
def chr_filter(value):
    """
    Convert a number to its corresponding ASCII character.
    Replaces the missing chr filter.
    """
    try:
        return chr(int(value))
    except (ValueError, TypeError, OverflowError):
        return ''
