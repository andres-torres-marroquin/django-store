from django.db import models

ENABLED_DISABLED_STATUSES = (
    (True, 'Enabled'),
    (False, 'Disabled'),
)


class Address(models.Model):
    pass


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
