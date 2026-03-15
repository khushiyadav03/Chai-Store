from django import forms

from .models import BulkOrderRequest, ContactMessage


INPUT_CLASS = "form-control"
TEXTAREA_CLASS = "form-control form-control-textarea"


class ContactMessageForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": INPUT_CLASS, "placeholder": "Email address"}),
            "phone": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Phone number"}),
            "message": forms.Textarea(
                attrs={"class": TEXTAREA_CLASS, "placeholder": "Tell us what you need", "rows": 5}
            ),
        }


class BulkOrderRequestForm(forms.ModelForm):
    class Meta:
        model = BulkOrderRequest
        fields = ["name", "org", "quantity", "date", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Your name"}),
            "org": forms.TextInput(attrs={"class": INPUT_CLASS, "placeholder": "Organization or event"}),
            "quantity": forms.NumberInput(attrs={"class": INPUT_CLASS, "placeholder": "Approx. cups"}),
            "date": forms.DateInput(attrs={"class": INPUT_CLASS, "type": "date"}),
            "message": forms.Textarea(
                attrs={"class": TEXTAREA_CLASS, "placeholder": "Order details", "rows": 4}
            ),
        }
