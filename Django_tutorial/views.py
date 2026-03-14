from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_POST

from chai.forms import BulkOrderRequestForm, ContactMessageForm
from chai.models import MenuItem, SiteContent, Testimonial


def _site_content():
    content = {item.key: item.value for item in SiteContent.objects.all()}
    return {
        "hero_tagline": content.get("hero_tagline", "Crafted with warmth. Served with soul."),
        "about_text": content.get(
            "about_text",
            "Chai. pours slow-brewed cups rooted in comfort, warmth, and everyday ritual. "
            "Every blend is built around fresh ingredients and careful steeping. "
            "The result is a modern chai experience that still feels familiar.",
        ),
        "hero_cta_primary": content.get("hero_cta_primary", "View Menu"),
        "hero_cta_secondary": content.get("hero_cta_secondary", "Find a Store"),
        "bulk_order_note": content.get(
            "bulk_order_note",
            "Planning an office serving or private event? Share the details and we will get back with a warm, practical quote.",
        ),
    }


def home(request):
    featured_items = MenuItem.objects.filter(is_available=True)[:3]
    testimonials = Testimonial.objects.all()[:4]
    context = {
        **_site_content(),
        "featured_items": featured_items,
        "testimonials": testimonials,
    }
    return render(request, "index.html", context)


def about(request):
    return HttpResponse("About Page")


def contact(request):
    context = {
        **_site_content(),
        "contact_form": ContactMessageForm(),
        "bulk_order_form": BulkOrderRequestForm(),
    }
    return render(request, "contact.html", context)


@require_POST
def contact_message_submit(request):
    form = ContactMessageForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"ok": True, "message": "Your message has been sent."})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)


@require_POST
def bulk_order_submit(request):
    form = BulkOrderRequestForm(request.POST)
    if form.is_valid():
        form.save()
        return JsonResponse({"ok": True, "message": "Your bulk order request has been sent."})
    return JsonResponse({"ok": False, "errors": form.errors}, status=400)
