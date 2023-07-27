from django.utils.text import slugify


def unique_slugify(value, model, field_name="slug"):
    base = slugify(value)
    slug = base
    i = 1
    while model.objects.filter(**{field_name: slug}).exists():
        slug = f"{base}-{i}"
        i += 1
    return slug
