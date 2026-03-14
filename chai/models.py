from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class ChaiVariety(models.Model):
    CHAI_TYPE_CHOICE = [
        ("ML", "MASALA"),
        ("GR", "GINGER"),
        ("KL", "KIWI"),
        ("PL", "PLAIN"),
        ("EL", "ELAICHI"),
    ]

    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="chais/")
    date_added = models.DateTimeField(default=timezone.now)
    type = models.CharField(max_length=2, choices=CHAI_TYPE_CHOICE)
    description = models.TextField(default="")

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class ChaiReview(models.Model):
    chai = models.ForeignKey(ChaiVariety, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    date_added = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-date_added"]

    def __str__(self):
        return f"{self.user.username} review for {self.chai.name}"


class MenuItem(models.Model):
    CATEGORY_CHOICES = [
        ("Classic", "Classic"),
        ("Masala", "Masala"),
        ("Cold", "Cold"),
        ("Special", "Special"),
    ]
    TAG_CHOICES = [
        ("", "None"),
        ("Bestseller", "Bestseller"),
        ("Seasonal", "Seasonal"),
        ("New", "New"),
    ]

    name = models.CharField(max_length=120)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to="menu/")
    tag = models.CharField(max_length=20, choices=TAG_CHOICES, blank=True, default="")
    is_available = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self):
        return self.name


class Store(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, default="")
    address = models.CharField(max_length=255, blank=True, default="")
    city = models.CharField(max_length=100, blank=True, default="")
    phone = models.CharField(max_length=30, blank=True, default="")
    opening_hours = models.CharField(max_length=100, blank=True, default="")
    google_maps_url = models.URLField(blank=True, default="")
    chai_varities = models.ManyToManyField(ChaiVariety, related_name="stores", blank=True)

    class Meta:
        ordering = ["city", "name"]

    @property
    def full_address(self):
        return self.address or self.location

    def __str__(self):
        return self.name


class ChaiCertificate(models.Model):
    chai = models.OneToOneField(ChaiVariety, on_delete=models.CASCADE, related_name="certificate")
    certificate_num = models.CharField(max_length=100)
    issued_date = models.DateTimeField(default=timezone.now)
    valid_till = models.DateTimeField()

    class Meta:
        ordering = ["-issued_date"]

    def __str__(self):
        return f"Certificate for {self.chai.name}"


class Testimonial(models.Model):
    customer_name = models.CharField(max_length=100)
    quote = models.TextField()
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    avatar = models.ImageField(upload_to="testimonials/", blank=True, null=True)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"{self.customer_name} ({self.rating}/5)"


class SiteContent(models.Model):
    key = models.CharField(max_length=100, unique=True)
    value = models.TextField()

    class Meta:
        verbose_name = "Site content"
        verbose_name_plural = "Site content"
        ordering = ["key"]

    def __str__(self):
        return self.key


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True, default="")
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Contact message from {self.name}"


class BulkOrderRequest(models.Model):
    name = models.CharField(max_length=100)
    org = models.CharField(max_length=150)
    quantity = models.PositiveIntegerField()
    date = models.DateField()
    message = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]

    def __str__(self):
        return f"Bulk order from {self.org} by {self.name}"
