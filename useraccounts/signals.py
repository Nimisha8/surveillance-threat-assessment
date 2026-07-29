from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import AuthorizedUser
from .face_utils import compute_encoding_from_image


@receiver(post_save, sender=AuthorizedUser)
def generate_encoding(sender, instance, created, **kwargs):
    """
    After an AuthorizedUser is saved, compute and store their face encoding
    from the uploaded photo (only if we don't already have one).
    """
    # Skip if no photo, or encoding already computed
    if not instance.photo:
        return
    if instance.encoding:
        return

    encoding = compute_encoding_from_image(instance.photo.path)
    if encoding is not None:
        instance.set_encoding(encoding)
        # Save just the encoding field; avoid re-triggering the signal loop
        AuthorizedUser.objects.filter(pk=instance.pk).update(encoding=instance.encoding)