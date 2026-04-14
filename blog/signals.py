from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from blog.models import Post, Profile

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)


@receiver(post_save, sender=Post)
def update_posts_count_on_create(sender, instance, created, **kwargs):
    if created:
        profile, _ = Profile.objects.get_or_create(user=instance.author)
        profile.posts_count += 1
        profile.save(update_fields=['posts_count'])
        print(f"New post created by {instance.author.username}")


@receiver(post_delete, sender=Post)
def update_posts_count_on_delete(sender, instance, **kwargs):
    profile, _ = Profile.objects.get_or_create(user=instance.author)
    profile.posts_count = max(profile.posts_count - 1, 0)
    profile.save(update_fields=['posts_count'])
    print(f"Post deleted: {instance.title}")
