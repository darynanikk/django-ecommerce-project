import django_filters
from django import forms

from store.models import Item

SIZES_CHOICES = [('S', 'Small'), ('M', 'Medium'), ('L', 'Large')]
FAVORITE_COLORS_CHOICES = [
    ('blue', 'Blue'),
    ('green', 'Green'),
    ('red', 'Red'),
    ('purple', 'Purple')
]


def is_valid_queryparam(param):
    return param != '' and param is not None


def item_filter(request):
    qs = Item.objects.all()
    data = request.GET
    option = data.get('option')
    if is_valid_queryparam(option):
        if option == 'name-asc':
            qs = qs.order_by('title')
        elif option == 'name-desc':
            qs = qs.order_by('-title')
        elif option == 'price-asc':
            qs = qs.order_by('price')
        elif option == 'price-desc':
            qs = qs.order_by('-price')
    return qs


class ItemsFilter(django_filters.FilterSet):
    sizes = django_filters.MultipleChoiceFilter(widget=forms.RadioSelect(),
                                                choices=SIZES_CHOICES)
    colours = django_filters.MultipleChoiceFilter(widget=forms.CheckboxSelectMultiple(), choices=FAVORITE_COLORS_CHOICES)

    class Meta:
        model = Item
        fields = {
            'categories',
            'sizes',
            'colours',
        }
