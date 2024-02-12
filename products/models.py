from django.db import models
from versatileimagefield.fields import VersatileImageField


def get_upload_path(*args):
    instance, filename = args
    ext = filename.split('.')[-1]
    filename = '{}.{}'.format(instance.slug, ext)
    path = f'covers/{instance.__class__.__name__.lower()}/'
    return '{}{}'.format(path, filename)


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AbstractCategory(TimeStampedModel):
    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at', 'title']
        abstract = True

    title = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100,
        unique=True,
    )
    cover = models.ImageField(
        upload_to=get_upload_path,
    )

    def __str__(self):
        return self.title


class Category(AbstractCategory):
    class Meta(AbstractCategory.Meta):
        verbose_name = 'category'
        verbose_name_plural = 'categories'


class SubCategory(AbstractCategory):
    class Meta(AbstractCategory.Meta):
        verbose_name = 'subcategory'
        verbose_name_plural = 'subcategories'

    category = models.ForeignKey(
        to=Category,
        on_delete=models.SET_NULL,
        null=True,
    )


class Product(TimeStampedModel):
    class Meta:
        get_latest_by = 'created_at'
        ordering = ['-created_at', 'title']

    title = models.CharField(max_length=100)
    slug = models.SlugField(
        max_length=100,
        unique=True,
    )
    price = models.DecimalField(max_digits=9, decimal_places=2)
    cover = VersatileImageField(upload_to=get_upload_path)
    subcategory = models.ForeignKey(
        to=SubCategory,
        on_delete=models.SET_NULL,
        null=True,
    )

    def __str__(self):
        return self.title
