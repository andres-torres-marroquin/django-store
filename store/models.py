from django.contrib.auth.models import User
from django.db import models

ENABLED_DISABLED_STATUSES = (
    (True, 'Enabled'),
    (False, 'Disabled'),
)


class Address(models.Model):
    customer = models.ForeignKey('Customer', related_name='addresses')
    first_name = models.CharField(max_length=30, null=True, blank=True)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    address_1 = models.CharField(max_length=128)
    address_2 = models.CharField(max_length=128)
    city = models.CharField(max_length=128)
    zip_code = models.CharField(max_length=10)
    #country = models.ForeignKey('Country')


class Customer(models.Model):
    user = models.OneToOneField('auth.User')
    telephone = models.CharField(max_length=14, null=True, blank=True)  # e.g. (123) 123-1234
    fax = models.CharField(max_length=14, null=True, blank=True)  # e.g. (123) 123-1234
    address = models.ForeignKey('Address', null=True, blank=True)
    ip = models.IPAddressField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_first_name(self):
        return self.user.first_name
    first_name = property(get_first_name)

    def get_last_name(self):
        return self.user.last_name
    last_name = property(get_last_name)


class CustomerIP(models.Model):
    customer = models.ForeignKey('Customer', related_name='ips')
    ip = models.IPAddressField()
    created_at = models.DateTimeField(auto_now_add=True)


class Category(models.Model):
    parent = models.ForeignKey('Category', related_name='children', null=True, blank=True)
    sort_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True, choices=ENABLED_DISABLED_STATUSES)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


class CategoryDescription(models.Model):
    category = models.ForeignKey('Category', related_name='descriptions')
    language = models.ForeignKey('Language', related_name='+')
    name = models.CharField(max_length=255)
    text = models.TextField()


class Product(models.Model):
    model = models.CharField(max_length=64)
    sku = models.CharField(max_length=64, null=True, blank=True)
    upc = models.CharField(max_length=12, null=True, blank=True)
    quantity = models.IntegerField(default=0)
    shipping = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=15, decimal_places=4, default='0.0000')
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    status = models.BooleanField(default=True, choices=ENABLED_DISABLED_STATUSES)
    viewed = models.IntegerField(default=0)
    related_products = models.ManyToManyField('self')
    categories = models.ManyToManyField('Category', related_name='products')


class ProductDescription(models.Model):
    product = models.ForeignKey('Product', related_name='descriptions')
    language = models.ForeignKey('Language', related_name='+')
    name = models.CharField(max_length=255)
    text = models.TextField()


class ProductImage(models.Model):
    product = models.ForeignKey('Product', related_name='images')
    image = models.ImageField(upload_to='product_images/')
    sort_order = models.IntegerField(default=0)


class ProductAttribute(models.Model):
    product = models.ForeignKey('Product', related_name='attributes')
    language = models.ForeignKey('Language', related_name='+')
    text = models.TextField()


class Language(models.Model):
    name = models.CharField(max_length=32, null=True, blank=True)
    code = models.CharField(max_length=5)
    sort_order = models.IntegerField(default=0)
    status = models.BooleanField(default=True, choices=ENABLED_DISABLED_STATUSES)


class Currency(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=3)
    symbol_left = models.CharField(max_length=12)
    symbol_right = models.CharField(max_length=12)
    decimal_place = models.IntegerField()
    value = models.DecimalField()
    status = models.BooleanField()
    date_modified = models.DateTimeField()

# User model monkey patching
def get_store_profile(user):
    if not hasattr(user, '_store_profile_cache'):
        profile, created = Customer.objects.get_or_create(user=user)
        user._store_profile_cache = profile
    return user._store_profile_cache
User.get_store_profile = get_store_profile
