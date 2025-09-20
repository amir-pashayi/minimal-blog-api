from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django_redis import get_redis_connection
from .models import Post, Category

def bust_cache():
    conn = get_redis_connection("default")
    for key in conn.scan_iter("mbapi:*"):
        conn.delete(key)

@receiver(post_save, sender=Post)
@receiver(post_delete, sender=Post)
def clear_cache_on_post_change(sender, instance, **kwargs):
    bust_cache()

@receiver(m2m_changed, sender=Post.categories.through)
def clear_cache_on_category_change(sender, instance, **kwargs):
    bust_cache()

@receiver(post_save, sender=Category)
@receiver(post_delete, sender=Category)
def clear_cache_on_category_update(sender, instance, **kwargs):
    bust_cache()
