from django import template

register = template.Library()

@register.filter
def format_phone(value):
    if not value:
        return ""
    
    digits = ''.join(filter(str.isdigit, value))
    if len(digits) == 10:
        return f"({digits[0:3]}) {digits[3:6]}-{digits[6:]}"
    elif len(digits) == 11 and digits.startswith('1'):
        return f"+1 ({digits[1:4]}) {digits[4:7]}-{digits[7:]}"
    else:
        return value
        