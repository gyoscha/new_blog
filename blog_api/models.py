from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField(
        "self",
        related_name="followed_by",
        symmetrical=False,
        blank=True
    )

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(instance, created, **kwargs):
    """ Функция создания профиля при создании пользователя и подписка на себя же """
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()


class Note(models.Model):
    """ Модель для записей """
    user = models.ForeignKey(
        User, related_name='note', on_delete=models.DO_NOTHING
    )
    title = models.CharField(
        max_length=300,
        verbose_name='Заголовок'
    )
    note = models.TextField(verbose_name='Текст поста')
    create_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return (
            f"{self.user} "
            f"({self.create_at:%Y-%m-%d %H:%M}): "
            f"{self.title[:20]}..."
        )
