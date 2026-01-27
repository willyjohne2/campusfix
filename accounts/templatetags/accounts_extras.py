from django import template

register = template.Library()


@register.filter
def mask_email(value):
    """Mask an email address leaving first letter and domain visible.
    Example: 'john.doe@example.com' -> 'j***@example.com'
    """
    if not value or "@" not in value:
        return value
    local, domain = value.split("@", 1)
    if len(local) <= 1:
        masked_local = "*"
    else:
        masked_local = local[0] + "***"
    return f"{masked_local}@{domain}"
