from django import template


register = template.Library()


@register.filter(name='reviews')
def reviews(value):
    if value == 1:
        return f'1 review'
    elif value == '':
        return 'No reviews'
    return f'{value} reviews'


