from django import template


register = template.Library()


@register.filter
def mark_keyword(value, arg):
    if arg:
        value_lower = value.lower()
        arg_lower = arg.lower()
        try:
            index = value_lower.index(arg_lower)
            arg_len = len(arg)
            new_value = value[:index]
            new_value = new_value + f'<strong class="text-warning">{arg}</strong>'
            new_value = new_value + value[index + arg_len:]
            return new_value
        except:
            pass
    return value

@register.filter
def filter_by_category(clippings, category):
    return [clipping for clipping in clippings if clipping.category == category]

