from django.shortcuts import get_object_or_404, render

from .models import ChaiVariety, MenuItem, Store


def all_chai(request):
    menu_items = MenuItem.objects.filter(is_available=True)
    categories = [choice[0] for choice in MenuItem.CATEGORY_CHOICES]
    return render(
        request,
        "chai/all_chai.html",
        {
            "menu_items": menu_items,
            "categories": categories,
        },
    )


def chai_detail(request, chai_id):
    chai = get_object_or_404(ChaiVariety.objects.prefetch_related("reviews", "stores"), pk=chai_id)
    return render(
        request,
        "chai/chai_detail.html",
        {"chai": chai, "certificate": getattr(chai, "certificate", None)},
    )


def chai_store_view(request):
    stores = Store.objects.all()
    return render(request, "chai/chai_stores.html", {"stores": stores})
