from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from .models import Product
from versatileimagefield.image_warmer import VersatileImageFieldWarmer
import io
import sys
from PIL import Image
from django.core.files.uploadedfile import InMemoryUploadedFile


@receiver(models.signals.post_delete, sender=Product)
def delete_product_cover(sender, instance, **kwargs):
    """
    Deletes ExampleImageModel image renditions on post_delete.
    """
    # Deletes Image Renditions
    instance.cover.delete_all_created_images()
    # Deletes Original Image
    instance.cover.delete(save=False)


@receiver(models.signals.post_save, sender=Product)
def warm_product_covers(sender, instance, **kwargs):
    """Ensures Product thumbnails are created post-save"""
    product_cover_warmer = VersatileImageFieldWarmer(
        instance_or_queryset=instance,
        rendition_key_set='product_cover',
        image_attr='cover',
    )
    num_created, failed_to_create = product_cover_warmer.warm()


def image_resized(image, h):
    name = image.name
    _image = Image.open(image)
    content_type = Image.MIME[_image.format]
    r = h / _image.size[1]  # ratio
    w = int(_image.size[0] * r)
    image_temporary_resized = _image.resize((w, h))
    file = io.BytesIO()
    image_temporary_resized.save(file, _image.format)
    file.seek(0)
    size = sys.getsizeof(file)
    return InMemoryUploadedFile(
        file,
        'ImageField',
        name,
        content_type,
        size,
        None,
    )


@receiver(pre_save, sender=Product, dispatch_uid='post.save_image')
def save_product_cover(sender, instance, **kwargs):
    instance.cover = image_resized(instance.cover, 500)

    # update cover
    if not instance._state.adding:
        # - replace old with new
        # - delete old
        # - replace old sized images with new
        old = sender.objects.get(pk=instance.pk).cover
        new = instance.cover
        if old and new and old.url != new.url:
            warm_product_covers(sender=sender, instance=instance)
            old.delete_sized_images()
            old.delete(save=False)
