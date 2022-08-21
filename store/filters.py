from store.models import Item


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